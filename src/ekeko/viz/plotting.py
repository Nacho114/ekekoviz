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

def add_volume(fig, stock_df, visible):
    """Add volume bars to the plot."""
    colors = [COLORS['green'] if open < close else COLORS['red'] for open, close in zip(stock_df['Open'], stock_df['Close'])]

    fig.add_trace(
        go.Bar(
            x=stock_df.index, y=stock_df['Volume'],
            marker_color=colors,
            marker_line_width=0,
            name='Volume',
            hoverinfo='none',
            opacity=0.6,
            visible=visible
        ),
        secondary_y=True
    )

    # Update the secondary y-axis range to be at most 15% of the plot height
    fig.update_yaxes(
        title_text="Volume",
        secondary_y=True,
        range=[0, stock_df['Volume'].max() * 5],  # Scale factor to adjust the height
        showgrid=False,
        zeroline=False
    )
    
    # Update layout to adjust the margin between the main plot and volume plot
    fig.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        # height=700  # Adjust height as needed
    )
    
    return fig

def add_candlestick(fig, stock_df, visible):
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
            visible=visible
        )
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def add_buysell(fig, buysell_df):
    """Add buy/sell markers to the plot."""
    buys = buysell_df[buysell_df['Type'] == 'BUY']
    sells = buysell_df[buysell_df['Type'] == 'SELL']
    
    fig.add_trace(
        go.Scatter(
            x=buys['Date'],
            y=buys['Price'],
            mode='markers',
            marker=dict(
                symbol='triangle-up', 
                size=14, 
                color=COLORS['green'],
                line=dict(color='black', width=2.5)  # Adding black border
            ),
            name='Buy',
            hoverinfo='text',
            text=[f'Buy<br>Price: {price}<br>Size: {size}' for price, size in zip(buys['Price'], buys['Size'])]
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=sells['Date'],
            y=sells['Price'],
            mode='markers',
            marker=dict(
                symbol='triangle-down', 
                size=14, 
                color=COLORS['red'],
                line=dict(color='black', width=2.5)  # Adding black border
            ),
            name='Sell',
            hoverinfo='text',
            text=[f'Sell<br>Price: {price}<br>Size: {size}' for price, size in zip(sells['Price'], sells['Size'])]
        )
    )
    
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

def plot(stock_df, curves=None, title="110", hide_candles_and_volume=True, buysell_df=None):
    """Plot stock data with additional curves and buy/sell markers."""
    plot_df = stock_df.copy()
    plot_df.index = plot_df.index.strftime('%Y-%m-%d')
    fig = init_stock_plot(title)

    visible = 'legendonly' if hide_candles_and_volume else True

    fig = add_candlestick(fig, plot_df, visible)
    
    fig = add_scatter(fig, plot_df.index, plot_df['Close'], 'close', 'blue', True)

    curve_colors = ['yellow', 'cyan', 'magenta']
    if curves:
        for idx, curve in enumerate(curves):
            color_index = idx % len(curve_colors)
            fig = add_scatter(fig, plot_df.index, curve['values'], curve['name'], curve_colors[color_index])

    fig = add_volume(fig, plot_df, True)

    if buysell_df is not None:
        fig = add_buysell(fig, buysell_df)
        
    return fig

def plot_different_stocks(stocks, price_type, title):
    """Plot different stocks on a single plot."""
    fig = init_stock_plot(title)

    curve_colors = ['blue', 'yellow', 'cyan', 'magenta']
    for idx, stock in enumerate(stocks):
        color_index = idx % len(curve_colors)
        dates = stock['df'].index.strftime('%Y-%m-%d')
        values = stock['df'][price_type]
        fig = add_scatter(fig, dates, values, stock['symbol'], curve_colors[color_index], visible=True)

    return fig
