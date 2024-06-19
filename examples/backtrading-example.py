import ekeko
from ekeko.backtrader import Logger, LoggingStrategy
import backtrader as bt

file_path  = '/home/nacho/code/ekeko/data/stooq/small-example-for-testing'
file_paths_from_dir = ekeko.dataloader.read_files_from_directory(file_path)

stooq_df = ekeko.stooq_to_df(file_paths_from_dir)

start_date = '2022-04-1'
end_date = '2024-06-18'
stock_df = stooq_df['gps']
stock_df = stock_df.loc[start_date:end_date]

# Define strategy

class SmaCross(LoggingStrategy):
    params = dict(
        pfast=10,
        pslow=30
    )

    def __init__(self, logger: Logger):
        super().__init__(logger)
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()
        super().next()  # Ensure to call the parent class's next method to log cash

data = bt.feeds.PandasData(dataname=stock_df)

# Initialize the 'Cerebro' engine
cerebro = bt.Cerebro()

# Add the data feed to Cerebro
cerebro.adddata(data)

# Create a logger instance
logger = Logger()

# Add the strategy, passing the logger instance
cerebro.addstrategy(SmaCross, logger)

# Run the strategy
cerebro.run()

# Extract data from the logger
buysell_df = logger.get_buy_sell_df()
trades_df = logger.get_trades_df()
cash_df = logger.get_cash_df()

fig = ekeko.viz.plot(stock_df, title="Stock Data with Buy/Sell", buysell_df=buysell_df)
fig.show()

print("Buy/Sell DataFrame:")
print(buysell_df)
print("\nTrades DataFrame:")
print(trades_df)
print("\nCash DataFrame:")
print(cash_df)
