import ekeko
import backtrader as bt
import pandas as pd

###############################
### Create fake data
###############################

# Create fake data
def create_fake_data(prices):
    num_days = len(prices)
    dates = pd.date_range(start='2022-01-01', periods=num_days, freq='D')
    df = pd.DataFrame(index=dates)
    df['Open'] = prices
    df['High'] = prices
    df['Low'] = prices
    df['Close'] = prices
    df['Volume'] = 1000
    return df

stock_dfs = {
    "STOCK_1": create_fake_data([2, 4, 6, -500, 3, 5]),
    "STOCK_2": create_fake_data([2, 4, 3, 1])
}

###############################
### Define Strategy
###############################

class EvenOddStrategy(bt.Strategy):
    def __init__(self):
        self.order = None

    def next(self):
        for data in self.datas:
            if data.close[0] % 2 == 0:  # Buy on even price
                if not self.getposition(data).size:
                    self.order = self.buy(data=data)

            if data.close[0] % 2 != 0 and data.close[0] > 0:  # Sell on odd price and on positive value
                if self.getposition(data).size:
                    self.order = self.sell(data=data)

###############################
### Run experiment
###############################

ekeko_cerebro = ekeko.backtrader.EkekoCerebro()
ekeko_cerebro.cerebro.broker.setcash(2000.0)

for ticker, stock_df in stock_dfs.items():
    print(ticker)
    ekeko_cerebro.adddata(stock_df, name=ticker)

ekeko_cerebro.addstrategy(EvenOddStrategy)

results, analysis_results = ekeko_cerebro.run()

def print_drawdown_analysis(drawdown_dict):
    def format_number(num):
        return f"{num:.2f}"

    def format_percentage(num):
        return f"{num}%"

    print("Drawdown Analysis:")
    print("\nCurrent Drawdown:")
    print(f"  Length: {drawdown_dict['len']} periods")
    print(f"  Percentage: {format_percentage(drawdown_dict['drawdown'])}")
    print(f"  Monetary Value: {format_number(drawdown_dict['moneydown'])} $nits")

    print("\nMaximum Drawdown:")
    print(f"  Length: {drawdown_dict['max']['len']} periods")
    print(f"  Percentage: {format_percentage(drawdown_dict['max']['drawdown'])}")
    print(f"  Monetary Value: {format_number(drawdown_dict['max']['moneydown'])} $")

    print("\nExplanations:")
    print("  Length: The duration of the drawdown in periods (e.g., days, weeks)")
    print("  Percentage: The drawdown expressed as a percentage of the peak value")
    print("  Monetary Value: The absolute decrease in value during the drawdown")
    print("\n  Current Drawdown: Represents the most recent or ongoing drawdown")
    print("  Maximum Drawdown: Represents the worst drawdown in the analyzed period")

def print_nice(analysis_dict):
    def print_dataframe(df):
        print(df.to_string())
        print()

    def print_nested_dict(d, indent=0):
        for key, value in d.items():
            print('  ' * indent + str(key) + ':')
            if isinstance(value, dict):
                print_nested_dict(value, indent+1)
            else:
                print('  ' * (indent+1) + str(value))

    print("=== Transactions ===")
    for ticker, df in analysis_dict['transactions'].items():
        print(f"Ticker: {ticker}")
        print_dataframe(df)

    print("=== Trades ===")
    for ticker, df in analysis_dict['trades'].items():
        print(f"Ticker: {ticker}")
        print_dataframe(df)

    print("=== Drawdown Analysis ===")
    print_drawdown_analysis(analysis_dict['drawdown'])

    print("=== Portfolio Analysis ===")
    print_nested_dict(analysis_dict['trade_analysis'])

print_nice(analysis_results)

