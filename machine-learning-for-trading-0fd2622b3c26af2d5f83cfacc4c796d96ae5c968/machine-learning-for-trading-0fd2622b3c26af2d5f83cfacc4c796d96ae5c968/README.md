# machine-learning-for-trading

##About this project
I wrote the majority of this project as several assignments for the Machine Learning for Trading course offered by Georgia Tech as a part of their online master's degree program. I've cleaned up the parts I thought were particularly interesting and published them here.

##Dependencies
You'll need Python 2.7 to run this project, as well as the following packages:
-Numpy+MKL
-matplotlib
-scipy
-pandas

[This site created by Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs/) is a great resource for getting all of the required packages. This is especially important for numpy - the standard "pip intall numpy" command does not contain all required libraries needed to install scipy. If you get an error trying to install scipy, just grab the link for numpy+mkl from this site instead. Make sure the version you select is appropriate for python 2.7 and your operating system. 

##About each section
Each folder in this project represents the work for a different unit in the course, though they all build upon one another in some way. 

###Unit 1
The first unit of the course was based around analyzing a stock portfolio and finding relevant information. The file analysis.py canculates the monetary value, portfolio statistics such as cumulative return, average daily return, and Sharpe Ratio (a measurement of risk-adjusted return that is calcuated by finding the average return earned in excess of the return rate on a risk-free investment). IT also contains method to print these helpful statistics and plot the normalized daily stock prices. Though the utility of this file is mostly that it is used in more complex operations later, you can also run it using the command `python -m Unit1.analysis` in the project's home directory. It will calculate statistics and graph the performance of a portfolio consisting of GOOG(20%), AAPL(20%), GLD(40%), and XOM(20%) stocks. 

Also in this Unit is optimization.py. When given a set of N stock ticker symbols, it uses scipy's optimize function to calculate what percentage of your portfolio funds you should invest in each stock in order to get an optimal return on your portfolio. It can be run using `python -m Unit1.optimization` in the project's home directory. THis will run the optimizer over a default set of stocks. If you want to specify your own stocks to include in a portfolio to be optimized, you can add the ticker symbols as separate arguments after calling the module - like `python -m Unit1.optimization GOOG AAPL XOM ...`. The program will check to make sure data for these stocks exist before optimizing, so make sure your symbol exists in the /data folder (though most commonly traded stocks do have data present!)

###Unit 2
This unit is based around the development of two trading strategies that make use of various technical indicators to predict when to buy, sell, or short shares of a given stock in order to maximize your beginning portfolio value. The first, bollinger_strategy.py, determines when to trade purely based on bollinger bands, or the bands marking two standard deviations above and below the simple moving average price of the stock. Bollinger Bands are typically used as part of a trading strategy to determine if a fluctuation in price is large enough to be of interest to investors. When the price of the stock moves outside of the Bollinger band, this denotes that this change is likely significant and represents an actual change in company value as opposed to the small daily fluctuations that arise from natural market movement.  The movement outside the band indicates it might be a good time to buy, sell, or short the stock in question, depending on where the band is crossed.  The result of such a strategy over the stock IBM for the time period of Dec 31, 2007 to Dec 31, 2009 can be seen in the graph below. 

![Bollinger Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMBollingerStrategy.png)

The vertical lines on the chart denote trades – red lines indicate a beginning to short sell a stock, green lines indicate buying a stock to hold long-term, and black lines indicate exits of either a short or long position. All of the trades were for 100 stocks each.  

And here's a graph of the value of this portfolio over time, compared to the value of the S&P 500 over the same time period and the same starting funds of $10,000

![Bollinger Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMBollingerValue.png)

This graph was obtained using use backtesting, a process by which all of the trades recommended by the strategy are fed into an order book, and a simulation is run from the beginning of the time period as if we’d actually followed the recommendations of the strategy and traded when it told us to. The backtesting methods can be found in the file trade_simulator.py.

You can run this program yourself using the command `python -m Unit2.bollinger_strategy ???` where ??? is the ticker symbol of the stock you'd like to develop a strategy for. Excluding this parameter defaults the stock to IBM

The second strategy found in my_strategy.py makes use of two additional technical indicators. The first is momentum. Momentum indicates the direction in which the stock is moving by comparing the current price of the stock to the price some number of days (here, 5) in the past. Stocks whose prices are trending upward will have a positive momentum, and vice versa. Additionally, the value of the momentum indicates how strongly the price is rising or falling. Momentum ranges from -0.5 to 0.5, with values farther from zero indicating more drastic change.

The second indicator relies on comparing Bollinger values, which are equivalent to (Daily Stock Price - Rolling Mean)/Rolling Standard Deviation. When the Bollinger value for the stock falls below the Bollinger value for the S&P 500, it is likely the stock price has fallen below what the general market activity predicts it should have. This technique makes the assumption that eventually the stock will return closer to the market average, at which point it can be sold for a profit. The result of such a strategy over the stock IBM for the time period of Dec 31, 2007 to Dec 31, 2009 can be seen in the graph below. 

![My Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMMyStrategy.png)

And here's a graph of the value of this portfolio over time, compared to the value of the S&P 500 over the same time period and the same starting funds of $10,000

![My Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMMyValue.png)

As you can see, my strategy outperforms the simple Bollinger band based strategy ($4058 profit versus $3614). This is the case for most stocks.

You can run this program yourself using the command `python -m Unit2.bollinger_strategy ???` where ??? is the ticker symbol of the stock you'd like to develop a strategy for. Again, the default is IBM.  

###Unit 3
The final portion of this project also uses a trading strategy to generate predictions on when it would be best to buy, sell, or short a given stock. Only instead of looking only at past stock data only, it makes use of a K-Nearest Neighbors learner to predict a stock price 5 days in the future and determine whether to buy, sell, or short that stock based on this predicted difference in price. My learner uses four different indicators to measure similarity between points - Bollinger Values, momentum, volatility (or, the rolling standard deviation of the stock price, which measures how intensely the stock price is fluctuating) and normalized stock price. The learner then finds the Euclidean distance between the trading data and the test data points, and finds the K (here defaulted to 3) nearest neighbors to make a prediction. A set of data is provided for training, and then an independent set is used to test. 

As an example, here are the graphs showing the performance of the trading strategy over IBM stock. The model is trained from Dec 31 2007 to 2009, and tested over the time period Dec 31 2009 to Dec 31 2011. The performance over the test data is shown.

![My Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMPredVsActual.png)

Shown here is the predicted stock price of the test set in comparison to the actual stock price.

![My Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMKNNStrategy.png)

Here are the trades generated by the strategy, similar to the graphs in the previous unit. 

![My Strategy graph](https://github.com/arwarner/machine-learning-for-trading/raw/master/data/images/IBMKNNValue.png)

And here is the profit earned by the trading strategy compared to the S&P 500. 

You can run this program by using the command `python -m Unit3.testlearner`. Optionally, you can also provide a stock ticker symbol following the command to run the learner for a specific stock. 

###Data
Stock price data including open, high, low, close, adjusted close, and volume traded for most major stocks. If a stock isn't included in here, you can't run the program over it!

###Utils
Contains some basic helper functions. 


##What's next? 
As a part of this class I created a Q-learning agent applicable to a generic path-finding problem. I'm in the process of adjusting this file to work with stock data as well, so that it can be used in a similar fashion to how the KNN learner is used in Unit 3 to find when the best opportunity to buy or sell a stock would be. I'm interested to see it's performance in comparison to the KNN learner!
