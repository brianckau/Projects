import pandas as pd
import numpy as np
from pygooglenews import GoogleNews
from transformers import pipeline
import yfinance as yf

def fetch_google_news(query:str, start_date:str, end_date:str):

    news = GoogleNews(lang='en',country='US')

    max_length = 0

    df = pd.DataFrame()

    for day in pd.date_range(start_date,end_date,freq='D'):
        length = len(news.search(query,when=day.strftime("%Y-%m-%d")).get("entries",[]))
        if length > max_length:
            max_length = length
        
    for day in pd.date_range(start_date,end_date,freq='D'):
        df[f'{day.year}-{day.month}-{day.day}'] = [np.nan for x in range(max_length)]

    for day in pd.date_range(start_date,end_date,freq='D'):
        entries = news.search(query, when=day.strftime("%Y-%m-%d")).get("entries",[])
        titles = [e.get("title") for e in entries]
        df.loc[:len(titles)-1,f'{day.year}-{day.month}-{day.day}'] = titles
    return df

def sentiment_analysis(query: str, start_date: str, end_date: str, mode):
    
    classifier = pipeline("sentiment-analysis")

    df = fetch_google_news(query, start_date, end_date)

    for col in df.columns:
        outcol = f"{col} Analysis"
        df.loc[:,outcol] = np.nan

        for row in range(len(df)):
            text = df.loc[row, col]
            if pd.isna(text):
                continue
            if mode == "score":
                df.loc[row, outcol] = classifier(str(text))[0]["score"]
            elif mode == "label":
                df.loc[row, outcol] = classifier(str(text))[0]["label"]
    return df


def news_count_volatility_analysis(series, ticker):
    series = series.copy()
    series.index = pd.to_datetime(series.index)
    if getattr(series.index, "tz", None) is not None:
        series.index = series.index.tz_localize(None)

    stock_data = yf.download(
        tickers=ticker,
        start=pd.to_datetime(series.index[0]),
        end=pd.to_datetime(series.index[-1]),
    )["Close"].pct_change().abs()[f"{ticker}"]

    stock_data = stock_data.copy()
    stock_data.index = pd.to_datetime(stock_data.index)
    if getattr(stock_data.index, "tz", None) is not None:
        stock_data.index = stock_data.index.tz_localize(None)

    news_vol_df = pd.concat([stock_data.rename("stock"), series.rename("Number of News")], axis=1).dropna()

    fig, ax = plt.subplots(figsize=(15, 6))

    ax2 = ax.twinx()  
    l1, = ax.plot(series.index, series.values, color="blue", alpha=0.9, lw=1, label="Number of News")
    l2, = ax2.plot(stock_data.index, stock_data.values, color="red", alpha=0.9, lw=1, label=f"{ticker} close price")

    ax.set_title(f"{ticker} Absolute Return (Volatility) & Number of Related News")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Related News")
    ax2.set_ylabel("Absolute Return")

    ax.legend(handles=[l1, l2], loc="upper left")
    plt.show()

    print(f'Correlation: {round(news_vol_df['stock'].corr(news_vol_df['Number of News']),4)}')

    return news_vol_df