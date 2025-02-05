import pandas as pd
from fredapi import Fred
from datetime import datetime
import os

# You'll need to set your FRED API key
# Get one from: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = 'your_api_key_here'
fred = Fred(api_key=FRED_API_KEY)

# Define the series IDs and their descriptions
series_mapping = {
    'GS10': 'TREASURY_YIELD',
    'CPIAUCSL': 'CPI_INDEX',  # Consumer Price Index for All Urban Consumers
    'GDP': 'GDP',  # Gross Domestic Product
    'MORTGAGE30US': 'MORTGAGE_30_US_FIXED',  # 30-Year Fixed Rate Mortgage Average
    'UNRATE': 'UNRATE',  # Unemployment Rate
    'INDPRO': 'INDPRO_INDEX',  # Industrial Production Index
    'UMCSENT': 'UMCSENT_INDEX',  # University of Michigan: Consumer Sentiment
    'CSUSHPINSA': 'CSUSHPINSA_INDEX',  # Case-Shiller U.S. National Home Price Index
    'CP': 'CP_INDEX',  # Corporate Profits After Tax
    'FEDFUNDS': 'FEDFUNDS_RATE'  # Effective Federal Funds Rate
}

def fetch_fred_data(start_date='1960-01-01', end_date='2015-12-31'):
    """
    Fetch economic data from FRED for the specified date range.

    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format

    Returns:
        pandas.DataFrame: DataFrame containing all the economic indicators
    """
    # Convert dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize an empty dictionary to store the series
    data_dict = {}

    # Fetch each series
    for series_id, column_name in series_mapping.items():
        try:
            # Fetch the data
            series = fred.get_series(series_id, start, end)
            data_dict[column_name] = series
            print(f"Successfully fetched {column_name}")
        except Exception as e:
            print(f"Error fetching {column_name}: {str(e)}")
            data_dict[column_name] = pd.Series(dtype='float64')  # Empty series if fetch fails

    # Combine all series into a single DataFrame
    df = pd.DataFrame(data_dict)

    # Forward fill missing values (some series might have different frequencies)
    df = df.fillna(method='ffill')

    # Backward fill any remaining missing values at the start
    df = df.fillna(method='bfill')

    return df

def main():
    # Create the output directory if it doesn't exist
    output_dir = 'fred_data'
    os.makedirs(output_dir, exist_ok=True)

    # Fetch the data
    df = fetch_fred_data()

    # Save to CSV
    output_file = os.path.join(output_dir, 'economic_indicators_1960_2015.csv')
    df.to_csv(output_file)
    print(f"\nData saved to {output_file}")

    # Display basic statistics
    print("\nDataset Overview:")
    print(f"Time period: {df.index.min()} to {df.index.max()}")
    print(f"Number of records: {len(df)}")
    print("\nMissing values summary:")
    print(df.isnull().sum())

if __name__ == "__main__":
    main()
