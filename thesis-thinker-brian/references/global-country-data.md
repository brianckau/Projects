# Global and country factor data

The two files below cover October 2021 through September 2026. Each contains one row per date or month and keeps the same global factor columns for all stocks.

- [Daily CSV](../assets/global-country-daily-5y.csv) contains 1,254 aligned US trading sessions.
- [Monthly CSV](../assets/global-country-monthly-5y.csv) contains 60 observations.
- All return columns are decimal simple returns. The benchmark and global style columns are in USD. Native cash columns use the currency named in the header. Missing values are blank.

| Column | Source and construction |
|---|---|
| `market_return` | USD adjusted closing return on [Vanguard Total World Stock ETF (VT)](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf), a proxy for developed and emerging equity markets. Adjusted close history from [Yahoo Finance](https://finance.yahoo.com/quote/VT/history/). |
| `mkt_rf`, `rf` | VT return less USD cash. USD cash is the corresponding daily or monthly RF series from the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). |
| `smb`, `hml`, `mom` | The French library's developed-market three-factor size and value series and developed-market momentum. Monthly values are native published monthly factor returns. |
| `country_<code>_return_usd` | Adjusted close returns from Yahoo Finance for the listed USD ETF proxies. Daily returns use consecutive US trading closes. Monthly returns use consecutive month-end US trading closes. ETF fees, tracking, market hours, and methodology changes can affect the proxy. |
| `rf_hkd` | [HKMA 30-day Exchange Fund Bill yield](https://apidocs.hkma.gov.hk/documentation/market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-yield-daily/) as a short-rate accrual proxy. |
| `rf_gbp` | [Bank of England SONIA, IUDSOIA](https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxIRx&SeriesCodes=IUDSOIA) as an overnight accrual proxy. |
| `rf_eur` | [ECB €STR](https://data.ecb.europa.eu/data/datasets/EST/EST.B.EU000A2X2A25.WT) as an overnight accrual proxy for euro-area countries. |
| `rf_cad` | [Bank of Canada CORRA, AVG.INTWO](https://www.bankofcanada.ca/rates/interest-rates/corra/) as an overnight accrual proxy. |

The local cash proxies accrue calendar-day simple interest using the latest rate dated before the accrual day. The day-count base is 360 for EUR and 365 for HKD, GBP, and CAD. Returns compound across the daily or monthly holding period. The HKD calculation approximates cash accrual from yield. It does not measure mark-to-market bill returns. USD uses the published RF series as supplied. Other local cash currencies require separate verified data.

Country code to ETF mapping:

| Market group | Country code and ticker |
|---|---|
| Americas | US VTI, CA EWC, MX EWW, BR EWZ, CL ECH, PE EPU |
| Asia Pacific | HK EWH, CN MCHI, JP EWJ, SG EWS, TW EWT, KR EWY, AU EWA, IN INDA, ID EIDO, TH THD, MY EWM, PH EPHE, VN VNM |
| Europe | GB EWU, DE EWG, FR EWQ, IT EWI, ES EWP, CH EWL, NL EWN, SE EWD, BE EWK, AT EWO, IE EIRL, DK EDEN, FI EFNL, NO ENOR, GR GREK, PL EPOL, TR TUR |
| Middle East and Africa | IL EIS, ZA EZA, SA KSA, AE UAE, QA QAT |

The global model can run for any stock with sufficient aligned USD return history. Country beta needs a valid country benchmark. Use the custom country file for uncovered markets. Choose the country intentionally for cross-listed or multinational companies and report the effective sample and input sources.
