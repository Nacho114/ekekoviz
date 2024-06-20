import ekeko
from ekeko.backtrader import Logger, LoggingStrategy
import backtrader as bt
import pandas as pd
import numpy as np

###############################
### Load data
###############################

file_path  = '/home/nacho/code/ekeko/data/stooq/small-example-for-testing'
file_paths_from_dir = ekeko.dataloader.read_files_from_directory(file_path)

stooq_df = ekeko.stooq_to_df(file_paths_from_dir)

start_date = '2022-04-1'
end_date = '2024-06-18'
stock_df = stooq_df['gps']
stock_df = stock_df.loc[start_date:end_date]

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

data = bt.feeds.PandasData(dataname=stock_df) # type: ignore

# Initialize the 'Cerebro' engine
cerebro = bt.Cerebro()

# Add the data feed to Cerebro
cerebro.adddata(data)

# Create a logger instance
logger = Logger()

# Add the strategy, passing the logger instance
cerebro.addstrategy(EmaCross, logger)

# Run the strategy
results = cerebro.run()

###############################
### Extract ema series
###############################

strategy = results[0]

ema_fast = pd.Series(np.array(strategy.ema_fast.array), name ='ema_fast', index=stock_df.index)
ema_slow = pd.Series(np.array(strategy.ema_slow.array), name ='ema_slow', index=stock_df.index)

curves = []
curves.append(ema_fast)
curves.append(ema_slow)

###############################
### Extract logger results
###############################

# Extract data from the logger
buysell_df = logger.get_buy_sell_df()
trades_df = logger.get_trades_df()
cash_df = logger.get_cash_df()

###############################
### Curves to plot
###############################

fig = ekeko.viz.plot(stock_df, curves, title="Stock Data with Buy/Sell", buysell_df=buysell_df)
fig.show()

