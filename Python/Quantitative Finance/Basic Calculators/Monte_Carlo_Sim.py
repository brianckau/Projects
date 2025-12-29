import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

print("European Option Pricing with Monte Carlo Simulation\n")

ticker = input("Enter the Ticker: ")
price = yf.Ticker(ticker).history(period = "5Y", interval = "1D").Close[-1]
volatility = yf.Ticker(ticker).history(period = "5Y", interval = "1D").Close.pct_change().std()*np.sqrt(252)

print(f'Current Stock Price for {ticker} is {round(price,2)}\n')
print(f'Annual Volatility of {ticker} is {volatility*100}%')
So = price
K = float(input("Enter the Strike Price: "))
T = float(input("Enter the Time to Maturity: "))
r = float(input("Enter the Risk Free Rate: "))/100
sigma = volatility



number_of_simulations = 100
trading_days = 252

dt = T/trading_days

Z = np.random.standard_normal(size=(number_of_simulations,trading_days))

St = np.zeros((number_of_simulations, trading_days+1))

St[:,0] = So

payoff = np.zeros((number_of_simulations))

for i in range(trading_days):
  St[:,i+1] = St[:,i] * np.exp((r-0.5*sigma**2)*dt+sigma*dt**0.5*Z[:,i])
  payoff = np.maximum(St[:-1]-So,0)

avg_payoff = np.mean(payoff)

Option_Price = np.exp(-r*T)*avg_payoff

print(f"\n\n The Fair Value of the Option is {round(Option_Price,2)}.\n\n")

fig, ax = plt.subplots(1,1,constrained_layout = True)

fig.suptitle(f"European Option Pricing for {ticker}'s Option With Strike Price at {K}")

ax.set_title(f"Brownian Motion Price Simulation for {ticker}")
for j in range(number_of_simulations):
  ax.plot(St[j,:], linewidth = 0.7)
