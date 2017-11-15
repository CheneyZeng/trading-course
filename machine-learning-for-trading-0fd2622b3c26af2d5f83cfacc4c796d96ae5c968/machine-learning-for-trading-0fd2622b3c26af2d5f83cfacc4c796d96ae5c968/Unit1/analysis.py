"""A set of helper functions for analyzing the content and performance of a stock portfolio"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from utils.util import get_data, plot_data


"""Computes the daily portfolio value given daily prices for each stock in portfolio, initial allocations(as fractions that sum to 1) and total starting value invested in portfolio"""
def get_portfolio_value(prices, allocs, start_val=1):
    #normalize all of the prices
    df = prices / prices.ix[0] 
    #multiply the normed values by the allocations to each of the equities
    df = df * allocs
    #multiply your allocated values by the start value
    df = df * start_val
    #determine the entire portfolio value on each day by summing all of the columns. 
    port_val = df.sum(axis=1)
    return port_val


"""Calculates the cumulative return, average daily return (and standard deviation) and Sharpe ratio of a portfolio
given the daily portfolio values, the daily risk-free rate of return, and the frequency of sampling (or, how many trading days there are)"""
def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    #cumulative return - how much portfolio has gone up from the beginning of time to the end
    cum_ret = (port_val[-1]/port_val[0])-1

    #to calculate the avg daily return, std dev of daily return, and sharpe ratio, we need to first find the daily returns
    daily_returns = port_val.copy()
    daily_returns = (daily_returns/daily_returns.shift(1)) - 1
    daily_returns.ix[0, 0] = 0 #set the first number to 0, instead of it's current value of NaN

    #average daily return - how much return on investment a stock makes on average daily (+stddev)
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()

    #sharpe ratio - average return earned in excess of the risk-free rate per unit of volatility or total risk
    sharpe_ratio = ((daily_returns - daily_rf).mean()/daily_returns.std()) * np.sqrt(samples_per_year)

    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


"""Normalize given stock prices and plot for comparison,g iven a data frame of stock prices to plot, and plot title and labeling information"""
def plot_normalized_data(df, title="Normalized prices", xlabel="Date", ylabel="Normalized price"):
    df = df/df.ix[0]
    ax = df.plot(title = title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.grid(True, 'both')
    plt.show()


"""Simulate and assess the performance of a stock portfolio."""
def assess_portfolio(start_date, end_date, symbols, allocs, start_val=1):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = get_portfolio_value(prices, allocs, start_val)

    #Get portfolio statistics (note: std_daily_ret = volatility)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with SPY using a normalized plot
    df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and SPY")


"""Though this class is mostly used for helper functions, you can execute all of them here for testing.
Some default options are provided, though these can be changed to the stock, allocation, and date of your choice. """
def test_run():
    start_date = '2010-01-01'
    end_date = '2010-12-31'

    symbol_allocations = OrderedDict([('GOOG', 0.2), ('AAPL', 0.2), ('GLD', 0.4), ('XOM', 0.2)])
    symbols = symbol_allocations.keys()
    allocs = symbol_allocations.values()
    start_val = 1000000

    assess_portfolio(start_date, end_date, symbols, allocs, start_val)


if __name__ == "__main__":
    test_run()
