# -*- coding: utf-8 -*-
"""ekekoviz

A small library to plot financial stock data using Plotly.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration section for colors and styling
COLORS = {
    'background': "#22262f",
    'text': '#8f98af',
    'grid_line': '#323641',
    'green': '#30cc5a',
    'red': '#f03538'
}
GRID_N_TICKS = 10

def init_stock_plot(title):
    """Initialize a stock plot with a secondary y-axis."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        hovermode='x',
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        xaxis=dict(
            type='category',
            tickformat='%b %Y',
            showgrid=True,
            gridcolor=COLORS['grid_line'],
            gridwidth=1,
            griddash='dot',
            nticks=GRID_N_TICKS,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['grid_line'],
            gridwidth=1,
            griddash='dot',
            nticks=GRID_N_TICKS
        ),
        yaxis2=dict(
            showgrid=False,
        ),
        font=dict(color=COLORS['text']),
    )
    return fig

def add_volume(fig, stock_df):
    """Add volume bars to the plot."""
    max_volume = stock_df['Volume'].max() * 1.5
    colors = [COLORS['green'] if open < close else COLORS['red'] for open, close in zip(stock_df['Open'], stock_df['Close'])]

    fig.add_trace(
        go.Bar(
            x=stock_df.index, y=stock_df['Volume'],
            marker_color=colors,
            marker_line_width=0,
            name='Volume',
            hoverinfo='none',
            opacity=0.6
        ),
        secondary_y=True
    )
    fig.update_yaxes(title_text="Volume", secondary_y=True, range=[0, max_volume])
    return fig

def add_candlestick(fig, stock_df):
    """Add candlestick plot to the figure."""
    fig.add_trace(
        go.Candlestick(
            x=stock_df.index,
            open=stock_df['Open'],
            high=stock_df['High'],
            low=stock_df['Low'],
            close=stock_df['Close'],
            increasing_line_color=COLORS['green'],
            decreasing_line_color=COLORS['red'],
            name='Candlestick',
        )
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def add_scatter(fig, dates, values, name, color, visible='legendonly'):
    """Add scatter plot to the figure."""
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            name=name,
            line=dict(color=color, width=2),
            visible=visible
        )
    )
    return fig

def plot(stock_df, curves, title):
    """Plot stock data with additional curves."""
    plot_df = stock_df.copy()
    plot_df.index = plot_df.index.strftime('%Y-%m-%d')
    fig = init_stock_plot(title)
    fig = add_candlestick(fig, plot_df)

    curve_colors = ['blue', 'yellow', 'cyan', 'magenta']
    for idx, curve in enumerate(curves):
        color_index = idx % len(curve_colors)
        fig = add_scatter(fig, plot_df.index, curve['values'], curve['name'], curve_colors[color_index])

    fig = add_volume(fig, plot_df)
    return fig

def plot_different_stocks(stocks, price_type, title):
    """Plot different stocks on a single plot."""
    fig = init_stock_plot(title)

    curve_colors = ['blue', 'green', 'cyan', 'magenta', 'yellow']
    for idx, stock in enumerate(stocks):
        color_index = idx % len(curve_colors)
        dates = stock['df'].index.strftime('%Y-%m-%d')
        values = stock['df'][price_type]
        fig = add_scatter(fig, dates, values, stock['symbol'], curve_colors[color_index], visible=True)

    return fig
