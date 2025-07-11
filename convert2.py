import csv
from datetime import datetime

### 
# Convert the Bitcoin_5yr.csv to the format of the other csv files
###

# Read the input file
with open('data/Bitcoin_5yr.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    data = []
    for row in reader:
        if len(row) < 5:
            continue
        date_str, close_str, open_str, high_str, low_str, *_ = row
        # Parse date
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        time_iso = dt.strftime('%Y-%m-%dT00:00:00.000Z')
        # Parse prices, remove commas
        open_price = float(open_str.replace(',', ''))
        high_price = float(high_str.replace(',', ''))
        low_price = float(low_str.replace(',', ''))
        close_price = float(close_str.replace(',', ''))
        data.append((dt, time_iso, open_price, high_price, low_price, close_price))

# Sort by date ascending
data.sort(key=lambda x: x[0])

# Write output as tab-delimited
with open('data/BTCUSD_5y.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['time', 'open', 'high', 'low', 'close'])
    for _, time_iso, open_p, high_p, low_p, close_p in data:
        writer.writerow([time_iso, open_p, high_p, low_p, close_p])