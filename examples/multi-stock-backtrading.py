import ekeko
from ekeko.backtrader import Logger, LoggingStrategy
import backtrader as bt
import pandas as pd
import numpy as np
import yfinance as yf

###############################
### Load data
###############################
 
tickers = ["GPS", "AAPL"]
period="5y"
start_date = '2022-04-1'
end_date = '2024-06-18'

###############################
### Define Strategy
###############################

class EmaCross(LoggingStrategy):
    params = dict(
        pfast=11,
        pslow=40
    )

    def __init__(self, logger: Logger):
        super().__init__(logger)
        # Define the fast and slow exponential moving averages
        self.ema_fast = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.pfast) # type: ignore
        self.ema_slow = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.pslow) # type: ignore

    def next(self):
        # Example trading logic based on EMA crossovers
        if self.ema_fast > self.ema_slow:
            # Buy signal
            if not self.position:
                self.buy()
        elif self.ema_fast < self.ema_slow:
            # Sell signal
            if self.position:
                self.sell()
        super().next()

###############################
### Run experiment
###############################

experiment_results = {}
for ticker in tickers:
    stock = yf.Ticker(ticker)
    stock_df = stock.history(period=period)
    stock_df = stock_df.loc[start_date:end_date]

    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=stock_df) # type: ignore
    cerebro.adddata(data)

    logger = Logger()

    cerebro.addstrategy(EmaCross, logger)

    results = cerebro.run()

    strategy = results[0]

    ema_fast = pd.Series(np.array(strategy.ema_fast.array), name ='ema_fast', index=stock_df.index)
    ema_slow = pd.Series(np.array(strategy.ema_slow.array), name ='ema_slow', index=stock_df.index)

    curves = []
    curves.append(ema_fast)
    curves.append(ema_slow)

    buysell_df = logger.get_buy_sell_df()

    plotting_data = {
        'stock_df': stock_df,
        'other_dfs': curves,
        'buysell_df': buysell_df,
        'title': ticker
    }


    performance = ekeko.backtrader.SingleStockPerformance(ticker, logger, strategy, data.close[0])

    experiment_results[ticker] = {
        'plotting_data': plotting_data,
        'performance': performance
    }

for ticker in tickers:
    print('-'*34)
    print('-'*34)
    fig = ekeko.viz.plot(**experiment_results[ticker]['plotting_data'])
    print(experiment_results[ticker]['performance'])
    #fig.show()

