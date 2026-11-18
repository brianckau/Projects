#!/usr/bin/env python3
"""Estimate market beta and four-factor exposure from adjusted prices."""
import argparse
import csv
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import io
import json
import math
from pathlib import Path
import tempfile
import urllib.request
import zipfile

BUNDLED_FACTORS = Path(__file__).resolve().parent.parent / "assets"
CACHE_DIRECTORY = Path.home() / ".cache/thesis-thinker/factors"
LIBRARY = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
REGIONS = {
    "us": ("F-F_Research_Data_Factors", "F-F_Momentum_Factor"),
    "global": ("Developed_3_Factors", "Developed_Mom_Factor"),
    "apac-ex-japan": ("Asia_Pacific_ex_Japan_3_Factors", "Asia_Pacific_ex_Japan_MOM_Factor"),
}


def french_rows(url, daily, momentum):
    with urllib.request.urlopen(url, timeout=20) as response:
        raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError("Factor archive exceeds size limit.")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        files = [item for item in archive.infolist() if item.filename.lower().endswith(".csv")]
        if len(files) != 1 or files[0].file_size > 4_000_000:
            raise ValueError("Unexpected factor archive contents.")
        content = archive.read(files[0]).decode("latin-1")
    rows = {}
    for row in csv.reader(content.splitlines()):
        if not row:
            continue
        key = row[0].strip()
        if not key.isdigit() or len(key) != (8 if daily else 6):
            continue
        if len(row) < (2 if momentum else 5):
            raise ValueError("Missing columns in factor archive.")
        values = tuple(float(x) for x in row[1:2 if momentum else 5])
        if any(not math.isfinite(x) or x <= -99 for x in values):
            continue
        period = datetime.strptime(key, "%Y%m%d" if daily else "%Y%m").date()
        rows[period.isoformat() if daily else period.strftime("%Y-%m")] = [x / 100 for x in values]
    if not rows:
        raise ValueError("No usable factor returns in archive.")
    return rows


def cache_factors(region, frequency, directory, refresh):
    paths = REGIONS[region]
    daily = frequency == "daily"
    suffix = ("_daily" if region == "us" else "_Daily") if daily else ""
    urls = [f"{LIBRARY}{stem}{suffix}_CSV.zip" for stem in paths]
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{region}-{frequency}.csv"
    if refresh or not target.exists():
        core = french_rows(urls[0], daily, False)
        mom = french_rows(urls[1], daily, True)
        dates = sorted(core.keys() & mom.keys())
        if not dates:
            raise ValueError("The factor archives have no common dates.")
        with tempfile.NamedTemporaryFile("w", dir=directory, newline="", delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.writer(stream)
            writer.writerow(["date", "mkt_rf", "smb", "hml", "rf", "mom"])
            writer.writerows([key, *core[key], *mom[key]] for key in dates)
        temporary.replace(target)
    return target, urls


def build_snapshot(frequency, directory, output, refresh):
    regions = {}
    columns = ("mkt_rf", "smb", "hml", "mom", "rf")
    for region in REGIONS:
        path, _ = cache_factors(region, frequency, directory, refresh)
        regions[region] = read_csv(path, columns, frequency == "daily")
    latest = min(max(rows) for rows in regions.values())
    if frequency == "daily":
        end = date.fromisoformat(latest)
        # Clamp leap day when the corresponding earlier year has no February 29.
        day = 28 if (end.month, end.day) == (2, 29) else end.day
        cutoff = end.replace(year=end.year - 5, day=day)
        earliest = (cutoff + timedelta(days=1)).isoformat()
    else:
        year, month = map(int, latest.split("-"))
        start_year, month_index = divmod(year * 12 + month - 60, 12)
        earliest = f"{start_year:04}-{month_index + 1:02}"
    output.mkdir(parents=True, exist_ok=True)
    target = output / f"factors-{frequency}-5y.csv"
    with tempfile.NamedTemporaryFile("w", dir=output, newline="", delete=False) as stream:
        temporary = Path(stream.name)
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("date", "region", "market_return", *columns))
        for region, rows in regions.items():
            for period in sorted(rows):
                if earliest <= period <= latest:
                    values = [Decimal(f"{value:.4f}") for value in rows[period]]
                    market = values[0] + values[-1]
                    writer.writerow((period, region, f"{market:.4f}", *(f"{value:.4f}" for value in values)))
    temporary.replace(target)
    return target


def read_csv(path, columns, daily, region=None, skip_missing=False):
    rows = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not {"date", *columns}.issubset(reader.fieldnames or []):
            raise ValueError(f"{path.name} requires date and {', '.join(columns)} columns.")
        if region and "region" not in (reader.fieldnames or []):
            raise ValueError(f"{path.name} has no region column.")
        for row in reader:
            if region and row["region"] != region:
                continue
            key = row["date"]
            check = date.fromisoformat(key if daily else f"{key}-01")
            if key != (check.isoformat() if daily else check.strftime("%Y-%m")):
                raise ValueError("Use YYYY-MM-DD for daily dates and YYYY-MM for monthly factors.")
            if skip_missing and any(row[column] in ("", None) for column in columns):
                continue
            values = tuple(float(row[column]) for column in columns)
            if key in rows or not all(math.isfinite(value) for value in values):
                raise ValueError(f"Duplicate date or invalid number in {path.name}: {key}")
            rows[key] = values
    if not rows:
        raise ValueError(f"No observations in {path.name}" + (f" for {region}." if region else "."))
    return rows


def load_prices(path, symbol, start, end):
    if path:
        rows = {key: row[0] for key, row in read_csv(path, ("adj_close",), True).items()}
    else:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise ValueError("Ticker downloads require yfinance. Supply --prices or install yfinance.") from exc
        history = yf.Ticker(symbol).history(
            start=start - timedelta(days=45), end=end + timedelta(days=1),
            interval="1d", auto_adjust=True, actions=False,
        )
        rows = {stamp.date().isoformat(): float(close) for stamp, close in history["Close"].dropna().items()}
    if not rows or min(rows.values()) <= 0 or not all(map(math.isfinite, rows.values())):
        raise ValueError("No usable positive adjusted prices.")
    return rows


def price_returns(prices, daily, end, factor_periods):
    keys = sorted(key for key in prices if key <= end.isoformat())
    if daily:
        previous = dict(zip(factor_periods[1:], factor_periods))
        return {
            now: prices[now] / prices[prior] - 1
            for prior, now in zip(keys, keys[1:]) if previous.get(now) == prior
        }
    closes = {}
    for key in keys:
        closes[key[:7]] = key
    result = {}
    for prior, now in zip(sorted(closes), sorted(closes)[1:]):
        this_month = date.fromisoformat(now + "-01")
        next_month = (this_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        last_day = next_month - timedelta(days=1)
        prior_day = this_month - timedelta(days=1)
        now_close, prior_close = closes[now], closes[prior]
        if (end >= last_day and prior == prior_day.strftime("%Y-%m")
                and (last_day - date.fromisoformat(now_close)).days <= 7
                and (prior_day - date.fromisoformat(prior_close)).days <= 7):
            result[now] = prices[now_close] / prices[prior_close] - 1
    return result


def estimate(matches, factors, returns, columns):
    import numpy as np

    if len(matches) <= len(columns) + 1:
        raise ValueError(f"Insufficient matched observations: {len(matches)}.")
    y = np.array([returns[key] - factors[key][-1] for key in matches])
    x = np.array([[1, *factors[key][:len(columns)]] for key in matches])
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1] or np.ptp(y) == 0:
        raise ValueError("Regression is rank deficient or stock excess returns are constant.")
    residual = y - x @ beta
    # Bartlett-weighted Newey–West standard errors, in matched observation order.
    lag = int(4 * (len(matches) / 100) ** (2 / 9))
    scores = x * residual[:, None]
    meat = scores.T @ scores
    for offset in range(1, lag + 1):
        cross = scores[offset:].T @ scores[:-offset]
        meat += (1 - offset / (lag + 1)) * (cross + cross.T)
    gram_inverse = np.linalg.pinv(x.T @ x)
    covariance = gram_inverse @ meat @ gram_inverse
    errors = np.sqrt(np.maximum(np.diag(covariance), 0))
    return {
        "hac_lags": lag,
        "hac_standard_errors": dict(zip(columns, map(float, errors[1:]))),
        "alpha_per_period": float(beta[0]),
        "loadings": dict(zip(columns, map(float, beta[1:]))),
        "r_squared": float(1 - (residual @ residual) / np.sum((y - y.mean()) ** 2)),
    }


def country_model(matches, factors, returns, names, country_returns):
    """Remove the shared global factors from the USD country excess return."""
    if len(matches) <= len(names) + 2:
        raise ValueError("Insufficient common periods for the country model.")
    country_excess = {key: country_returns[key][0] for key in matches}
    projection = estimate(matches, factors, country_excess, names)
    loadings = projection["loadings"]
    augmented = {}
    for key in matches:
        *global_factors, rf = factors[key]
        fitted = projection["alpha_per_period"] + sum(
            loadings[name] * value for name, value in zip(names, global_factors)
        )
        residual = country_excess[key] - rf - fitted
        augmented[key] = (*global_factors, residual, rf)
    result = estimate(matches, augmented, returns, (*names, "country_residual"))
    result["country_projection_r_squared"] = projection["r_squared"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    cache = sub.add_parser("cache", help="Download official factor CSVs into a reusable local cache.")
    cache.add_argument("--region", choices=REGIONS, required=True)
    cache.add_argument("--frequency", choices=("daily", "monthly", "both"), default="both")
    cache.add_argument("--directory", type=Path, default=CACHE_DIRECTORY)
    cache.add_argument("--refresh", action="store_true")

    snapshot = sub.add_parser("snapshot", help="Build the two five-year factor tables from official archives.")
    snapshot.add_argument("--directory", type=Path, default=CACHE_DIRECTORY)
    snapshot.add_argument("--output", type=Path, required=True)
    snapshot.add_argument("--refresh", action="store_true")

    fit = sub.add_parser("fit")
    source = fit.add_mutually_exclusive_group(required=True)
    source.add_argument("--prices", type=Path)
    source.add_argument("--symbol")
    fit.add_argument("--currency", required=True, help="Currency of the adjusted price series.")
    fx = fit.add_mutually_exclusive_group()
    fx.add_argument("--fx", type=Path, help="Daily CSV with date,adj_close. FX quote must convert stock currency to factor currency.")
    fx.add_argument("--fx-symbol", help="Optional FX ticker for yfinance.")
    fit.add_argument("--fx-invert", action="store_true", help="Use when FX is quoted as stock currency units per factor currency unit.")
    fit.add_argument("--factor-currency", default="USD", help="Currency of the factor or custom benchmark series. Official factors use USD.")
    factor_source = fit.add_mutually_exclusive_group(required=True)
    factor_source.add_argument("--factors", type=Path, help="Single-region factor CSV, custom or downloaded.")
    factor_source.add_argument("--region", choices=REGIONS, help="Use the bundled factor table for this region.")
    factor_source.add_argument("--global-model", action="store_true", help="Use the bundled world market and global style factors.")
    fit.add_argument("--global-data", type=Path, help="Override the bundled VT and global style CSV when using --global-model.")
    country_source = fit.add_mutually_exclusive_group()
    country_source.add_argument("--country", type=str.lower, help="Country code for a bundled USD country benchmark, with --global-model.")
    country_source.add_argument("--country-file", type=Path, help="Custom date,country_return_usd CSV, with --global-model.")
    fit.add_argument("--frequency", choices=("daily", "monthly"), required=True)
    fit.add_argument("--start", type=date.fromisoformat, required=True)
    fit.add_argument("--end", type=date.fromisoformat, required=True)
    fit.add_argument("--market-only", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "cache":
            frequencies = ("daily", "monthly") if args.frequency == "both" else (args.frequency,)
            for frequency in frequencies:
                path, urls = cache_factors(args.region, frequency, args.directory, args.refresh)
                print(json.dumps({"path": str(path), "sources": urls,
                                  "cached_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()}))
            return
        if args.command == "snapshot":
            for frequency in ("daily", "monthly"):
                print(build_snapshot(frequency, args.directory, args.output, args.refresh))
            return
        if args.start > args.end:
            raise ValueError("Start date must precede or equal end date.")
        factor_currency = args.factor_currency.upper()
        if args.global_data and not args.global_model:
            raise ValueError("--global-data requires --global-model.")
        if (args.country or args.country_file) and (not args.global_model or args.market_only):
            raise ValueError("Country beta requires --global-model and the full factor regression.")
        if (args.region or args.global_model) and factor_currency != "USD":
            raise ValueError("Bundled factors are in USD.")
        snapshot_name = "global-country" if args.global_model else "factors"
        factor_path = args.factors or args.global_data or BUNDLED_FACTORS / f"{snapshot_name}-{args.frequency}-5y.csv"
        daily = args.frequency == "daily"
        names = ("mkt_rf",) if args.market_only else ("mkt_rf", "smb", "hml", "mom")
        factors = read_csv(factor_path, (*names, "rf"), daily, args.region)
        country_returns = None
        if args.country or args.country_file:
            country_column = f"country_{args.country}_return_usd" if args.country else "country_return_usd"
            country_returns = read_csv(args.country_file or factor_path, (country_column,), daily, skip_missing=True)
        prices = load_prices(args.prices, args.symbol, args.start, args.end)
        if args.currency.upper() != factor_currency:
            if not (args.fx or args.fx_symbol):
                raise ValueError("Stock and factor currencies differ. Supply FX data.")
            rates = load_prices(args.fx, args.fx_symbol, args.start, args.end)
            prices = {key: prices[key] * (1 / rates[key] if args.fx_invert else rates[key])
                      for key in prices.keys() & rates.keys()}
        elif args.fx or args.fx_symbol or args.fx_invert:
            raise ValueError("Stock prices already match the factor currency.")
        returns = price_returns(prices, daily, args.end, sorted(factors))
        fmt = "%Y-%m-%d" if daily else "%Y-%m"
        first_allowed = args.start
        if not daily and args.start.day != 1:
            first_allowed = (args.start.replace(day=28) + timedelta(days=4)).replace(day=1)
        candidate_periods = {key for key in factors
                             if first_allowed.strftime(fmt) <= key <= args.end.strftime(fmt)}
        matches = sorted(candidate_periods & returns.keys())
        global_matches = matches
        if country_returns is not None:
            matches = sorted(set(matches) & country_returns.keys())
        minimum = 60 if daily else 24
        if len(matches) < (10 if daily else 8):
            raise ValueError(f"Insufficient matched {args.frequency} observations: {len(matches)}.")
        print(json.dumps({
            "frequency": args.frequency, "currency": factor_currency, "observations": len(matches),
            "first_period": matches[0], "last_period": matches[-1],
            "factor_periods_without_aligned_stock_return": len(candidate_periods) - len(global_matches),
            "periods_dropped_for_country_coverage": len(global_matches) - len(matches),
            "low_sample_warning": len(matches) < minimum,
            "stock_source": str(args.prices) if args.prices else f"Yahoo Finance via yfinance: {args.symbol}",
            "factor_file": str(factor_path), "factor_region": args.region,
            "global_market_benchmark": "VT" if args.global_model else None,
            "country": args.country,
            "country_file": str(args.country_file) if args.country_file else None,
            "factor_first_period": min(factors), "factor_last_period": max(factors),
            "fx_source": str(args.fx) if args.fx else args.fx_symbol,
            "market_model": estimate(matches, factors, returns, ("mkt_rf",)),
            "four_factor_model": None if args.market_only else estimate(matches, factors, returns, names),
            "global_plus_country_model": (
                country_model(matches, factors, returns, names, country_returns)
                if country_returns is not None else None
            ),
        }, indent=2))
    except (ValueError, OSError, KeyError, ImportError, zipfile.BadZipFile) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    main()
