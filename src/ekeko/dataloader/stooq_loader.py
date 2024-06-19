import pandas as pd
import os

def stooq_to_df(file_paths):
    """
    Converts a list of stooq data files into a dictionary of DataFrames.
    
    Parameters:
    file_paths (list): List of file paths to the stooq data files.
    
    Returns:
    dict: Dictionary where keys are ticker symbols and values are DataFrames.
    """
    # Initialize a dictionary to store DataFrames
    dataframes = {}

    # Load each file into a DataFrame
    for file_path in file_paths:
        # Read the CSV content from the file into a DataFrame
        df = pd.read_csv(file_path, delimiter=',')  # assuming tab-separated values

        # Rename columns to match yfinance DataFrame
        df.rename(columns={
            '<DATE>': 'Date',
            '<OPEN>': 'Open',
            '<HIGH>': 'High',
            '<LOW>': 'Low',
            '<CLOSE>': 'Close',
            '<VOL>': 'Volume'
        }, inplace=True)

        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

        # Set the timezone to America/New_York
        df['Date'] = df['Date'].dt.tz_localize('America/New_York')

        # Set the 'Date' column as the index
        df.set_index('Date', inplace=True)

        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

        # Extract the ticker symbol from the file name (e.g., 'gps.us.txt' -> 'gps')
        file_name = os.path.basename(file_path)
        ticker = file_name.split('.')[0]

        # Set the ticker as the index name
        df.index.name = ticker

        # Store the DataFrame in the dictionary
        dataframes[ticker] = df

    return dataframes
