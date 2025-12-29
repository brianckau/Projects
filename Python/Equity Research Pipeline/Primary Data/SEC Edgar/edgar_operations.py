import pandas as pd
import requests as req
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import logging
import calendar
import numpy as np

headers = {"User-Agent":"abc@gmail.com"}

pd.options.display.float_format = (
    lambda x: "{:,.0f}".format(x) if int(x) == x else "{:,.2f}".format(x)
)

statement_keys_map = {
    "balance_sheet": [
        "balance sheet",
        "balance sheets",
        "statement of financial position",
        "consolidated balance sheets",
        "consolidated balance sheet",
        "consolidated financial position",
        "consolidated balance sheets - southern",
        "consolidated statements of financial position",
        "consolidated statement of financial position",
        "consolidated statements of financial condition",
        "combined and consolidated balance sheet",
        "condensed consolidated balance sheets",
        "consolidated balance sheets, as of december 31",
        "dow consolidated balance sheets",
        "consolidated balance sheets (unaudited)",
    ],
    "income_statement": [
        "income statement",
        "income statements",
        "statement of earnings (loss)",
        "statements of consolidated income",
        "consolidated statements of operations",
        "consolidated statement of operations",
        "consolidated statements of earnings",
        "consolidated statement of earnings",
        "consolidated statements of income",
        "consolidated statement of income",
        "consolidated income statements",
        "consolidated income statement",
        "condensed consolidated statements of earnings",
        "consolidated results of operations",
        "consolidated statements of income (loss)",
        "consolidated statements of income - southern",
        "consolidated statements of operations and comprehensive income",
        "consolidated statements of comprehensive income",
    ],
    "cash_flow_statement": [
        "cash flows statement",
        "cash flows statements",
        "statement of cash flows",
        "statements of consolidated cash flows",
        "consolidated statements of cash flows",
        "consolidated statement of cash flows",
        "consolidated statement of cash flow",
        "consolidated cash flows statements",
        "consolidated cash flow statements",
        "condensed consolidated statements of cash flows",
        "consolidated statements of cash flows (unaudited)",
        "consolidated statements of cash flows - southern",
    ],
}


def cik_matching_ticker(ticker, headers=headers):
    ticker = ticker.upper().replace(".","-")
    ticker_json = req.get('https://www.sec.gov/files/company_tickers.json', headers=headers).json()
    for company in ticker_json.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            return cik
    raise ValueError(f"Ticker {ticker} not found in SEC database")

def get_submission_data(ticker, headers=headers, only_filings_df=False):
    cik = cik_matching_ticker(ticker)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    company_json = req.get(url,headers=headers).json()
    if only_filings_df:
        return pd.DataFrame(company_json['filings']['recent'])
    return company_json

def get_filtered_filings(ticker, headers=headers, ten_k=True,just_accession_numbers=False):
    company_filings_df = get_submission_data(ticker,headers,only_filings_df=True)
    if ten_k:
        df = company_filings_df[company_filings_df['form'] == "10-K"]
    else:
        df = company_filings_df[company_filings_df['form'] == "10-Q"]
    if just_accession_numbers:
        df = df.set_index('reportDate')
        accession_df = df['accessionNumber']
        return accession_df
    else:
        return df
    
def get_financial_data(ticker,headers=headers):
    cik = cik_matching_ticker(ticker)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    data = req.get(url,headers=headers).json()
    return data

def facts_df(ticker, headers=headers):
    data = get_financial_data(ticker)
    us_gaap_data = data['facts']['us-gaap']
    df_data = []
    for fact, details in us_gaap_data.items():
        for unit in details['units']:
            for item in details['units'][unit]:
                row = item.copy()
                row["fact"] = fact
                df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])
    df = df.drop_duplicates(subset=["fact","end","val"])
    df.set_index("end",inplace=True)
    labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
    return df, labels_dict

def time_series_comparison(df,target_line,headers=headers):

    time_series_financials = df[df['fact']==target_line][['fact','val']]

    fig,ax = plt.subplots(figsize=(15,6))

    ax.plot(time_series_financials['val'],color="red",alpha=0.85,lw=1.5,label=f"{target_line}")
    ax.set_title(f"{target_line} change from {pd.to_datetime(time_series_financials.index[0]).year} to {pd.to_datetime(time_series_financials.index[-1]).year}")
    ax.set_xlabel('Date')
    ax.set_ylabel(f'{target_line}')
    ax.legend()
    plt.show()

def time_series_comparison_v2(df, target_lines, headers=headers, 
                          normalize=False, figsize=(15, 8), title=None):

    if isinstance(target_lines, str):
        target_lines = [target_lines]
    
    available_metrics = df.index.tolist()
    missing_metrics = [m for m in target_lines if m not in available_metrics]
    
    if missing_metrics:
        print(f"Warning: Metrics not found: {missing_metrics}")
        target_lines = [m for m in target_lines if m in available_metrics]
    
    if not target_lines:
        print(" rror: No valid metrics to plot")
        return None
    
    time_series_data = {}
    for metric in target_lines:
        series = df.loc[metric].dropna()
        if not series.empty:
            time_series_data[metric] = series
    
    if not time_series_data:
        print("Error: No valid data available")
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    for i, (metric, series) in enumerate(time_series_data.items()):
        color = colors[i % len(colors)]
        
        if normalize and not series.empty:
            normalized = (series / series.iloc[0]) * 100
            ax.plot(normalized.index, normalized.values, color=color, 
                   alpha=0.85, lw=1.8, label=f"{metric} (norm)", 
                   marker='o', markersize=5)
        else:
            ax.plot(series.index, series.values, color=color, 
                   alpha=0.85, lw=1.8, label=metric, 
                   marker='o', markersize=5)
    
    if title is None:
        metrics_str = ', '.join(target_lines[:3])
        if len(target_lines) > 3:
            metrics_str += f"... ({len(target_lines)} total)"
        title = f"Financial Metrics: {metrics_str}"
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value' + (' (Normalized to 100)' if normalize else ''), fontsize=12)
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()


def annual_facts(ticker, headers=headers):
    accession_nums = get_filtered_filings(
        ticker,ten_k=True,just_accession_numbers=True
    )
    df, label_dict = facts_df(ticker,headers)
    ten_k = df[df['accn'].isin(accession_nums)]   
    #ten_k = ten_k[ten_k.index.isin(accession_nums.index)]
    pivot = ten_k.pivot_table(values="val",columns="fact",index="end")
    pivot.rename(columns = label_dict,inplace=True)
    return pivot.T

def quarterly_facts(ticker, headers=headers):
    accession_nums = get_filtered_filings(
        ticker,ten_k=False,just_accession_numbers=True
    )
    df, label_dict = facts_df(ticker,headers)
    ten_q = df[df['accn'].isin(accession_nums)]
    ten_q = ten_q[ten_q.index.isin(accession_nums.index)]
    pivot = ten_q.pivot_table(values="val",columns="fact",index="end")
    pivot.rename(columns = label_dict,inplace=True)
    return pivot.T


def save_dataframe_to_csv(dataframe, folder_name, ticker, statement_name, frequency):
    directory_path = os.path.join(folder_name,ticker)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{statement_name}_{frequency}.csv")
    dataframe.to_csv(file_path)
    return None

def _get_file_name(report):
    html_file_name_tag = report.find("HtmlFileName")
    xml_file_name_tag = report.find("XmlFileName")

    if html_file_name_tag:
        return html_file_name_tag.text
    elif xml_file_name_tag:
        return xml_file_name_tag.text
    else:
        return ""


def _is_statement_file(short_name_tag, long_name_tag, file_name):
    return (
        short_name_tag is not None
        and long_name_tag is not None
        and file_name  
        and "Statement" in long_name_tag.text
    )


def get_statement_file_names_in_filing_summary(
    ticker, accession_number, headers=headers
):
    try:
        session = req.Session()
        cik = cik_matching_ticker(ticker)
        base_link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"
        filing_summary_link = f"{base_link}/FilingSummary.xml"
        filing_summary_response = session.get(
            filing_summary_link, headers=headers
        ).content.decode("utf-8")

        filing_summary_soup = BeautifulSoup(filing_summary_response, "lxml-xml")
        statement_file_names_dict = {}

        for report in filing_summary_soup.find_all("Report"):
            file_name = _get_file_name(report)
            short_name, long_name = report.find("ShortName"), report.find("LongName")

            if _is_statement_file(short_name, long_name, file_name):
                statement_file_names_dict[short_name.text.lower()] = file_name

        return statement_file_names_dict

    except req.RequestException as e:
        print(f"An error occurred: {e}")
        return {}


def get_statement_soup(
    ticker,
    accession_number,
    statement_name,
    headers,
    statement_keys_map,
):

    session = req.Session()

    cik = cik_matching_ticker(ticker)
    base_link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"

    statement_file_name_dict = get_statement_file_names_in_filing_summary(
        ticker, accession_number, headers
    )

    statement_link = None
    for possible_key in statement_keys_map.get(statement_name.lower(), []):
        file_name = statement_file_name_dict.get(possible_key.lower())
        if file_name:
            statement_link = f"{base_link}/{file_name}"
            break

    if not statement_link:
        raise ValueError(f"Could not find statement file name for {statement_name}")

    try:
        statement_response = session.get(statement_link, headers=headers)
        statement_response.raise_for_status()  # Check if the request was successful

        if statement_link.endswith(".xml"):
            return BeautifulSoup(
                statement_response.content, "lxml-xml", from_encoding="utf-8"
            )
        else:
            return BeautifulSoup(statement_response.content, "lxml")

    except req.RequestException as e:
        raise ValueError(f"Error fetching the statement: {e}")

 
def extract_columns_values_and_dates_from_statement(soup):

    columns = []
    values_set = []
    date_time_index = get_datetime_index_dates_from_statement(soup)

    for table in soup.find_all("table"):
        unit_multiplier = 1
        special_case = False

        table_header = table.find("th")
        if table_header:
            header_text = table_header.get_text()
            if "in Thousands" in header_text:
                unit_multiplier = 1
            elif "in Millions" in header_text:
                unit_multiplier = 1000
            if "unless otherwise specified" in header_text:
                special_case = True

        for row in table.select("tr"):
            onclick_elements = row.select("td.pl a, td.pl.custom a")
            if not onclick_elements:
                continue

            onclick_attr = onclick_elements[0]["onclick"]
            column_title = onclick_attr.split("defref_")[-1].split("',")[0]
            columns.append(column_title)

            values = [np.NaN] * len(date_time_index)

            for i, cell in enumerate(row.select("td.text, td.nump, td.num")):
                if "text" in cell.get("class"):
                    continue

                value = keep_numbers_and_decimals_only_in_string(
                    cell.text.replace("$", "")
                    .replace(",", "")
                    .replace("(", "")
                    .replace(")", "")
                    .strip()
                )
                if value:
                    value = float(value)
                    if special_case:
                        value /= 1000
                    else:
                        if "nump" in cell.get("class"):
                            values[i] = value * unit_multiplier
                        else:
                            values[i] = -value * unit_multiplier

            values_set.append(values)

    return columns, values_set, date_time_index


def get_datetime_index_dates_from_statement(soup: BeautifulSoup) -> pd.DatetimeIndex:

    table_headers = soup.find_all("th", {"class": "th"})
    dates = [str(th.div.string) for th in table_headers if th.div and th.div.string]
    dates = [standardize_date(date).replace(".", "") for date in dates]
    index_dates = pd.to_datetime(dates)
    return index_dates


def standardize_date(date: str) -> str:

    for abbr, full in zip(calendar.month_abbr[1:], calendar.month_name[1:]):
        date = date.replace(abbr, full)
    return date


def keep_numbers_and_decimals_only_in_string(mixed_string: str):

    num = "1234567890."
    allowed = list(filter(lambda x: x in num, mixed_string))
    return "".join(allowed)


def create_dataframe_of_statement_values_columns_dates(
    values_set, columns, index_dates
) -> pd.DataFrame:
    transposed_values_set = list(zip(*values_set))
    df = pd.DataFrame(transposed_values_set, columns=columns, index=index_dates)
    return df


def process_one_statement(ticker, accession_number, statement_name):
    try:
        soup = get_statement_soup(
            ticker,
            accession_number,
            statement_name,
            headers=headers,
            statement_keys_map=statement_keys_map,
        )
    except Exception as e:
        logging.error(
            f"Failed to get statement soup: {e} for accession number: {accession_number}"
        )
        return None

    if soup:
        try:
            columns, values, dates = extract_columns_values_and_dates_from_statement(
                soup
            )
            df = create_dataframe_of_statement_values_columns_dates(
                values, columns, dates
            )

            if not df.empty:
                df = df.T.drop_duplicates()
            else:
                logging.warning(
                    f"Empty DataFrame for accession number: {accession_number}"
                )
                return None

            return df
        except Exception as e:
            logging.error(f"Error processing statement: {e}")
            return None







































