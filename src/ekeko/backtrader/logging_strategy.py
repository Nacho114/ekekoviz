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
