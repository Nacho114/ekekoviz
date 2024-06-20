import pandas as pd
import backtrader as bt
from datetime import datetime

class Logger:

    def __init__(self):
        self.buy_sell = []
        self.trades = []
        self.cash = []

    def log_buy_sell(self, action: str, date: datetime, price: float, size: float):
        self.buy_sell.append({'Type': action, 'Date': date, 'Price': price, 'Size': size})

    def log_trade(self, date: datetime, pnl: float, pnlcomm: float):
        self.trades.append({'Type': 'TRADE', 'Date': date, 'PnL': pnl, 'PnL Comm': pnlcomm})

    def log_cash(self, date: datetime, cash: float):
        self.cash.append({'Type': 'CASH', 'Date': date, 'Cash': cash})

    def get_buy_sell_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.buy_sell)

    def get_trades_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.trades)

    def get_cash_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.cash)


class SingleStockPerformance:
    """
    A class that tracks and reports the performance of a trading strategy during backtesting.

    Attributes:
        unrealized_gain (float): The current unrealized gain of any open positions.
        open_position_value (float): The market value of open positions.
        realized_gain (float): The total realized gain from closed positions.
        sorted_trades_df (DataFrame): Dataframe of trades sorted by profit and loss.
        initial_cash (float): The initial cash amount at the start of backtesting.
        final_cash (float): The final cash amount at the end of backtesting.
        total_final_value (float): The total value at the end of backtesting, including cash and open positions.
    """
    
    def __init__(self, ticker: str, logger: Logger, strategy, close_price: float):
        self.ticker = ticker

        trades_df = logger.get_trades_df()
        cash_df = logger.get_cash_df()

        self.unrealized_gain = 0
        self.open_position_value = 0

        if strategy.position:
            size = strategy.position.size
            price = strategy.position.price
            self.unrealized_gain = (close_price - price) * size
            self.open_position_value = close_price * size

        self.realized_gain = trades_df['PnL'].sum()
        self.sorted_trades_df = trades_df.sort_values(by='PnL', ascending=False)
        self.initial_cash = cash_df['Cash'].iloc[0]
        self.final_cash = cash_df['Cash'].iloc[-1]
        self.total_final_value = self.final_cash + self.open_position_value

    def __str__(self):
        return (f"{self.ticker} Backtrading Performance Report:\n\n"
                f"Initial Cash: {self.initial_cash:.2f}\n"
                f"Final Cash: {self.final_cash:.2f}\n"
                f"Unrealized Gain: {self.unrealized_gain:.2f}\n"
                f"Open Position Value: {self.open_position_value:.2f}\n"
                f"Realized Gain: {self.realized_gain:.2f}\n"
                f"Total Final Value: {self.total_final_value:.2f}\n\n"
                f"Top Trades (PnL): \n{self.sorted_trades_df.head()}")

class LoggingStrategy(bt.Strategy):
    def __init__(self, logger: Logger):
        self.logger = logger
        super().__init__()

    def notify_order(self, order: bt.Order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.logger.log_buy_sell('BUY', self.data.datetime.date(0), order.executed.price, order.executed.size)
            elif order.issell():
                self.logger.log_buy_sell('SELL', self.data.datetime.date(0), order.executed.price, order.executed.size)

    def notify_trade(self, trade: bt.Trade):
        if trade.isclosed:
            self.logger.log_trade(self.data.datetime.date(0), trade.pnl, trade.pnlcomm)

    def next(self):
        self.logger.log_cash(self.data.datetime.date(0), self.broker.getcash())
        super().next()
