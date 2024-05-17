import yfinance as yf
import ekekoviz
# !<User notes>! Specify symbol and period of data to pull
# --------------------
symbol = "GPS"
period="4y"
# --------------------

stock = yf.Ticker(symbol)

stock_data = stock.history(period=period)

# !<User notes>! Specify your date range (this filters from loaded data!)
# --------------------
start_date = '2021-04-1'
end_date = '2023-05-22'
# --------------------

# Slice the DataFrame for the specified date range
stock_df = stock_data.loc[start_date:end_date]

curves = []

price = stock_df['Close']
curves.append({'values': price, 'name': 'Close'})

ema = price.ewm(span=20, adjust=False).mean()
curves.append({'values': ema, 'name': 'ema 20'})

ma = price.rolling(window=40, min_periods=1).mean()
curves.append({'values': ma, 'name': 'ma 40'})

fig = ekekoviz.plot(stock_df, curves, f'{symbol} Close price action')
fig.show()
