import ekeko
import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np

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

class EmaCross(bt.Strategy):
    params = dict(
        pfast=11,
        pslow=40
    )

    def __init__(self):
        self.ema_fast = {}
        self.ema_slow = {}

        for _, data in enumerate(self.datas):
            self.ema_fast[data._name] = bt.indicators.ExponentialMovingAverage(
                data.close, period=self.params.pfast) # type: ignore
            self.ema_slow[data._name] = bt.indicators.ExponentialMovingAverage(
                data.close, period=self.params.pslow) # type: ignore

    def next(self):
        for data in self.datas:
            name = data._name
            if self.ema_fast[name] > self.ema_slow[name]:
                # Buy signal
                if not self.getposition(data).size:
                    self.buy(data=data)
            elif self.ema_fast[name] < self.ema_slow[name]:
                # Sell signal
                if self.getposition(data).size:
                    self.sell(data=data)

###############################
### Run experiment
###############################

ekeko_cerebro = ekeko.backtrader.EkekoCerebro()
experiment_results = {}
stock_dfs = {}

for ticker in tickers:
    stock = yf.Ticker(ticker)
    stock_df = stock.history(period=period)
    stock_df = stock_df.loc[start_date:end_date]
    stock_dfs[ticker] = stock_df
    ekeko_cerebro.adddata(stock_df, name=ticker)

ekeko_cerebro.addstrategy(EmaCross)

results, analysis_results = ekeko_cerebro.run()

print(analysis_results)


curves_per_ticker = {}
for ticker in tickers:
    stock_df = stock_dfs[ticker]
    ema_fast = pd.Series(np.array(results.ema_fast[ticker].array), name ='ema_fast', index=stock_df.index)
    ema_slow = pd.Series(np.array(results.ema_slow[ticker].array), name ='ema_slow', index=stock_df.index)

    curves = []
    curves.append(ema_fast)
    curves.append(ema_slow)
    curves_per_ticker[ticker] = curves


ticker = tickers[1]
transactions = analysis_results['transactions']

fig = ekeko.viz.plot(stock_dfs[ticker], other_dfs=curves_per_ticker[ticker], transactions=transactions[ticker])
fig.show()

ekeko_cerebro.cerebro.plot()
