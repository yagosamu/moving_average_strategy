"""
Project 1: Anti-Crisis Strategy - Technical Analysis using Moving Averages on ALPA4

This script implements and backtests a moving average crossover trading strategy for the Brazilian stock ALPA4.
The strategy is compared to a buy-and-hold of ALPA4 and the Ibovespa index.

Author: Adapted from Python notebook to .py with English explanations.
"""

# Step 1 - Import Libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk

# Use the cyberpunk style for plots (optional, for aesthetics)
plt.style.use("cyberpunk")


# Step 2 - Download Data from Yahoo Finance
ticker = "ALPA4.SA"
start_date = "2021-05-27"
end_date = "2025-04-30"

# Download daily historical data for ALPA4
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

# Step 3 - Define Moving Average Windows
# Short (fast) and long (slow) window periods for moving averages (in days)
fast_window = 7
slow_window = 40

# Step 4 - Calculate Moving Averages
# Calculate the rolling (moving) averages for the adjusted close price
data["Fast MA"] = data["Adj Close"].rolling(window=fast_window).mean()
data["Slow MA"] = data["Adj Close"].rolling(window=slow_window).mean()

# Step 5 - Calculate Daily Returns
# Calculate the daily return as the percentage change in the adjusted close price
data["daily_return"] = data["Adj Close"].pct_change()

# Drop rows with NaN values created by rolling means or returns
data = data.dropna()

# Step 6 - Generate Buy/Sell Signals
# If the fast MA is above the slow MA, we are 'long' (buy, 1), else 'short' (sell, -1)
data["position"] = np.where(data["Fast MA"] > data["Slow MA"], 1, -1)
# To avoid lookahead bias, shift the position by 1 day (we act on the signal the next day)
data["position"] = data["position"].shift(1)
data = data.dropna()

# Step 7 - Calculate Model (Strategy) Returns
# The model return is the daily return times the position (1 for long, -1 for short)
data["strategy_return"] = data["daily_return"] * data["position"]
# Calculate cumulative returns for the strategy
data["cumulative_strategy_return"] = (1 + data["strategy_return"]).cumprod() - 1

# Step 8 - Calculate Asset and Ibovespa Returns for Comparison
# Cumulative return of simply holding ALPA4
data["cumulative_stock_return"] = (1 + data["daily_return"]).cumprod() - 1

# Download Ibovespa data for the same period
ibov = yf.download("^BVSP", start=data.index[0], end=end_date, auto_adjust=False)["Adj Close"]
# Calculate daily and cumulative returns for Ibovespa
data["ibov_return"] = ibov.pct_change().values[:len(data)]  # Ensure alignment
data["cumulative_ibov_return"] = (1 + data["ibov_return"]).cumprod() - 1

# Step 9 - Plot the Returns
plt.figure(figsize=(14, 7))
plt.plot(data["cumulative_strategy_return"], label="Moving Average Strategy")
plt.plot(data["cumulative_stock_return"], label="ALPA4 Buy & Hold")
plt.plot(data["cumulative_ibov_return"], label="Ibovespa")
plt.title("Cumulative Returns: Moving Average Strategy vs. ALPA4 vs. Ibovespa")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()

# Step 10 - (Optional) Optimize Parameters
# You can add code here to test different window sizes to find the best parameters for the strategy.