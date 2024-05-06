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
filtered_by_time_df = stock_data.loc[start_date:end_date]

ekekoviz.plot(filtered_by_time_df, f'{symbol} Close price action')

