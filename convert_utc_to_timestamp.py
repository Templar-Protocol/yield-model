import pandas as pd
from datetime import datetime
import os

def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.000Z')

def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert the 'time' column
    df['time'] = df['time'].apply(convert_timestamp)
    
    # Save the modified DataFrame back to a CSV file
    output_file = f"converted_{os.path.basename(file_path)}"
    df.to_csv(output_file, index=False)
    print(f"Converted {file_path} to {output_file}")

def main():
    csv_files = [
        'BTCUSD_Daily_OHLC.csv',
        'ETHUSD_1440.csv',
        'NEARUSD_1440.csv',
        'XRPUSD_1440.csv',
        'LTCUSD_1440.csv',
        'SOLUSD_1440.csv',
        'BONKUSD_1440.csv',
        'ADAUSD_1440.csv',
    ]

    for file in csv_files:
        if os.path.exists(file):
            process_csv(file)
        else:
            print(f"File not found: {file}")

if __name__ == "__main__":
    main()