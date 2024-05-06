# -*- coding: utf-8 -*-
"""ekekoviz

A small library to plot financial stock data
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Default colors
bg_color = "#22262f"
text_color = '#8f98af'
grid_line_color = '#323641'
grid_n_ticks = 10
red = '#f03538'
green = '#30cc5a'

def init_stock_plot(title):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        hovermode='x',
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(
            type='category',  # This enables dates with no data to be removed, data type is better but makes this complex.
            tickformat='%b %Y',
            showgrid=True,
            gridcolor=grid_line_color,
            gridwidth=1,
            griddash='dot',  # Dotted grid lines,
            nticks=grid_n_ticks,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_line_color,
            gridwidth=1,
            griddash='dot',  # Dotted grid lines,
            nticks=grid_n_ticks
        ),
        yaxis2=dict(
            showgrid=False,
        ),
        font=dict(color=text_color),
    )
    return fig

# Helper function to format volume
def format_volume(vol):
    if vol >= 1_000_000:
        return f"{vol / 1_000_000:.3f}M"
    elif vol >= 1000:
        return f"{vol / 1000:.3f}K"
    else:
        return f"{vol:.3f}"

def add_close_price(fig, stock_df):
    fig.add_trace(
        go.Scatter(
            x=stock_df.index,
            y=stock_df['Close'], name='Close',
            mode='lines',  # Use 'lines' to show only the line without markers
            hovertemplate=(
                "Date: %{x}<br>" +
                "Open: %{customdata[0]:.3f}<br>" +
                "High: %{customdata[1]:.3f}<br>" +
                "Low: %{customdata[2]:.3f}<br>" +
                "Close: %{customdata[3]:.3f}<br>" +
                "Volume: %{customdata[4]}<extra></extra>"
            ),
            customdata=np.stack((stock_df['Open'], stock_df['High'], stock_df['Low'], stock_df['Close'], stock_df['Volume'].apply(format_volume)), axis=-1)
        ),
        secondary_y=False  # Primary y-axis for price
    )
    fig.update_yaxes(title_text='Close', secondary_y=False)

    return fig

def add_volume(fig, stock_df):

    # Normalize secondary axis (this a half-assed solution)
    secondary_y_max = stock_df['Volume'].max() * 1.5

    # Determine colors based on whether the day closed higher or lower
    colors = [green if o < c else red for o, c in zip(stock_df['Open'], stock_df['Close'])]

    # Add the volume trace
    fig.add_trace(
        go.Bar(
            x=stock_df.index, y=stock_df['Volume'],
            marker_color=colors,
            marker_line_width=0,
            name='Volume',
            hoverinfo='none',
            opacity=0.6
        ),
        secondary_y=True  # Indicate that this trace uses the secondary y-axis
    )

    # Adjust the secondary y-axis range
    fig.update_yaxes(
        title_text="Volume",
        secondary_y=True,
        range=[0, secondary_y_max]  # Adjusted max value
    )

    return fig

def add_candlestick(fig, stock_df):
    fig.add_trace(
        go.Candlestick(
            x=stock_df.index,
            open=stock_df['Open'],
            high=stock_df['High'],
            low=stock_df['Low'],
            close=stock_df['Close'],
            increasing_line_color=green,
            decreasing_line_color=red,
            name='Candlestick',
            visible='legendonly'
        )
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def add_moving_average(fig, stock_df, window, color):
    moving_average = stock_df['Close'].rolling(window=window, min_periods=1).mean()
    fig.add_trace(
        go.Scatter(
            x=stock_df.index,
            y=moving_average,
            name=f'{window} day MA',
            line=dict(color=color, width=2),
            visible='legendonly'  # Initially hidden
        )
    )
    return fig

def add_exponential_moving_average(fig, stock_df, span, color):
    ema = stock_df['Close'].ewm(span=span, adjust=False).mean()
    fig.add_trace(
        go.Scatter(
            x=stock_df.index,
            y=ema,
            name=f'{span} day EMA',
            line=dict(color=color, width=2),
            visible='legendonly'  # Initially hidden
        )
    )
    return fig

def plot(stock_df, title):
    # Note: we re-index to make the x-axis index prettier, can't use native
    # date stlye in plotting, and need to use category instead which removes
    # empty days.
    stock_df.index = stock_df.index.strftime('%Y-%m-%d')

    fig = init_stock_plot(title)
    fig = add_close_price(fig, stock_df)
    fig = add_candlestick(fig, stock_df)

    # !<User notes>! Here are the MA and EMA definitions! Change them here :)
    # --------------------
    ema_short_window = 12
    ema_long_window = 150
    ma_window = 50
    # --------------------

    fig = add_exponential_moving_average(fig, stock_df, ema_short_window, 'yellow')
    fig = add_exponential_moving_average(fig, stock_df, ema_long_window, 'magenta')
    fig = add_moving_average(fig, stock_df, ma_window, 'blue')

    fig = add_volume(fig, stock_df)


    fig.show()


