import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import *
from matplotlib.font_manager import *
import yfinance as yf
from sentiment_fetch import *


def time_series_sentiment(df,query,sma_days):
    time_series = pd.Series(dtype="float64")

    epsilon = 1e-9

    for col in df.columns:
            if "Analysis" in col:
 
                counts = df[col].value_counts()
                
                n_positive = counts.get("POSITIVE", 0)
                n_negative = counts.get("NEGATIVE", 0)
                
                numerator = n_positive - n_negative
                denominator = n_positive + n_negative + epsilon
                
                time_series.loc[col] = numerator / denominator

    time_series.index = time_series.index.str.removesuffix(" Analysis")
    
    sma_time_series = time_series.rolling(window=sma_days).mean()
    sma_time_series.index = time_series.index

    fig, ax = plt.subplots(figsize=(15,8))

    ax.plot(time_series,color="blue",alpha=0.9,label=f"{query} News Sentiment",lw=1)
    ax.plot(sma_time_series,color="red",alpha=0.9,label=f"Smoothed {query} News Sentiment, SMA-{sma_days}",lw=1)

    ax.set(title=f"Time-Series Google News Sentiment Plot for {query}",
           xlabel="Date", ylabel="Sentiment Score")
    
    loc = AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(ConciseDateFormatter(loc))

    fp = FontProperties(family="Times New Roman",size=12,weight="bold")

    ax.legend(prop=fp)

    return time_series



def sentiment_returns_analysis(series, ticker):

    series = series.copy()
    series.index = pd.to_datetime(series.index)
    if getattr(series.index, "tz", None) is not None:
        series.index = series.index.tz_localize(None)

    stock_data = yf.download(
        tickers=ticker,
        start=pd.to_datetime(series.index[0]),
        end=pd.to_datetime(series.index[-1]),
    )["Close"][f"{ticker}"].pct_change().shift(-1)

    stock_data = stock_data.copy()
    stock_data.index = pd.to_datetime(stock_data.index)

    if getattr(stock_data.index, "tz", None) is not None:
        stock_data.index = stock_data.index.tz_localize(None)

    sentiment_returns_df = pd.concat([stock_data.rename("stock"), series.rename("sentiment")], axis=1).dropna()

    fig, ax = plt.subplots(figsize=(15, 6))

    ax2 = ax.twinx()  
    l1, = ax.plot(series.index, series.values, color="blue", alpha=0.9, lw=1, label="News Sentiment")
    l2, = ax2.plot(stock_data.index, stock_data.values, color="red", alpha=0.9, lw=1, label=f"{ticker} return %")

    ax.set_title(f"{ticker} price & related news sentiment")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sentiment Score")
    ax2.set_ylabel("Asset Return %")

    ax.legend(handles=[l1, l2], loc="upper left")
    plt.show()

    print(f'Correlation: {round(sentiment_returns_df['stock'].corr(sentiment_returns_df['sentiment']),4)}')

    return sentiment_returns_df



def get_daily_news_count(query,start_date,end_date):
    df = fetch_google_news(query,start_date,end_date)
    return df.count()


def news_count_volatility_analysis(series, ticker):
    series = series.copy()
    series.index = pd.to_datetime(series.index)
    if getattr(series.index, "tz", None) is not None:
        series.index = series.index.tz_localize(None) 
    series = series.sort_index()

    start = series.index.min().normalize()
    end = series.index.max().normalize() + pd.Timedelta(days=1)

    px = yf.download(tickers=ticker, start=start, end=end, progress=False)  

    if isinstance(px.columns, pd.MultiIndex):
        high = px[("High", ticker)] if ("High", ticker) in px.columns else px[(ticker, "High")]
        low  = px[("Low", ticker)]  if ("Low", ticker)  in px.columns else px[(ticker, "Low")]
    else:
        high = px["High"]
        low = px["Low"]

    stock_data = (high - low).rename("stock")  

    stock_data = stock_data.copy()
    stock_data.index = pd.to_datetime(stock_data.index)
    if getattr(stock_data.index, "tz", None) is not None:
        stock_data.index = stock_data.index.tz_localize(None)

    news_vol_df = pd.concat([stock_data, series.rename("Number of News")], axis=1).dropna()
    corr = news_vol_df["stock"].corr(news_vol_df["Number of News"])  

    fig, ax = plt.subplots(figsize=(15, 6))
    ax2 = ax.twinx()

    l1, = ax.plot(news_vol_df.index, news_vol_df["Number of News"], color="blue", alpha=0.9, lw=1, label="Number of News")
    l2, = ax2.plot(news_vol_df.index, news_vol_df["stock"], color="red", alpha=0.9, lw=1, label=f"{ticker} High-Low range")

    ax.set_title(f"{ticker} High-Low (Volatility) & Number of Related News")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Related News")
    ax2.set_ylabel("High-Low range")

    ax.legend(handles=[l1, l2], loc="upper left")
    plt.show()

    print(f"Correlation: {corr:.4f}")
    return news_vol_df

