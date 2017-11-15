"""A set of helper functions for optimizing the performance of a stock portfolio"""

import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo
from utils.util import get_data, plot_data
from analysis import get_portfolio_value, get_portfolio_stats


"""Find optimal allocations for a stock portfolio, optimizing for Sharpe ratio, given the daily prices for each stock in the portfolio"""
def find_optimal_allocations(prices):
    guess = 1.0/prices.shape[1]
    function_guess = [guess] * prices.shape[1]
    bnds = [[0,1] for _ in prices.columns]
    cons = ({ 'type': 'eq', 'fun': lambda function_guess: 1.0 - np.sum(function_guess) })
    result = spo.minimize(error_optimal_allocations, function_guess, args = (prices,), method='SLSQP', bounds = bnds, constraints = cons, options={'disp':True})
    allocs = result.x
    return allocs

"""A helper function for the above function to minimize over"""
def error_optimal_allocations(allocs, prices):
    port_val = get_portfolio_value(prices, allocs, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)
    error = sharpe_ratio * -1
    return error

"""optimizes portfolio allocations and then simulates the performance of that portfolio compared to standard index fund data"""
def optimize_portfolio(start_date, end_date, symbols):
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)

    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get optimal allocations
    allocs = find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations, if they don't sum to 1.0

    # Get daily portfolio value (already normalized since we use default start_val=1.0)
    port_val = get_portfolio_value(prices, allocs)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Optimal allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    normed_SPY = prices_SPY / prices_SPY.ix[0, :]
    df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_data(df_temp, title="Daily Portfolio Value and SPY")


"""Though this class is mostly used for helper functions, you can execute all of them here for testing.
Some default options are provided, though these can be changed to the stocks and date range of your choice."""
def test_run():
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['GOOG', 'AAPL', 'GLD', 'HNZ']

    if (len(sys.argv) > 1):
        symbols = []
        for i in range(1, len(sys.argv)):
            file_path = "data/" + sys.argv[i] + ".csv"
            # Check if that file exists
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                print "Data for the stock {} does not exist. Please reference stocks in the data folder, or run with no option provided".format(stock)
                return
            symbols.append(sys.argv[i])

    optimize_portfolio(start_date, end_date, symbols)

if __name__ == "__main__":
    test_run()
