# Templar Protocol Yield Calculator

This tool calculates the historical yield for templar protocol based on various parameters.

## Usage

1. Ensure you have Python installed on your system.
2. Setup virtual environment and install the required packages:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

### Running with user input
3. Run the script to get user input:
```bash
python3 user_input.py
```
4. Follow the interactive prompts to input parameters.

### Running the Web Server Locally

3. Start the FastAPI server:
    ```bash
    python3 main.py
    ```
   This will start the server on `http://localhost:8080`.

4. You can now send POST requests to the `/calculate_yield` endpoint to calculate yields.

The API will return a JSON object with the calculated historical yield as a percentage based on the input parameters and historical price data in the following format:
```json
{
  "yield_percentage": 5.645147234051933,
  "start_datetime": "2023-09-12T00:00:00.000Z",
  "end_datetime": "2024-09-11T00:00:00.000Z",
  "parameters": {
    "price_csv": "Bitcoin_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv",
    "num_loans_per_day": 5,
    "avg_initial_collateral_ratio": 1.5,
    "min_collateral_ratio": 1.2,
    "origination_fee_pct": 0.01,
    "liquidation_spread_pct": 0.7,
    "avg_repayment_days": 300,
    "avg_slippage_pct": 0.02,
    "avg_loan_amount": 1000
  }
}
```
5. You can also get a list of available cryptocurrency csv files that can be used for yield calculation by sending a GET request to the `/available_crypto` endpoint:
```bash
curl -X GET "http://localhost:8080/available_crypto"
```
This will return a JSON object with the list of available cryptocurrency csv files:
```json
{
    "available_crypto":["BTC_1y_cmc","ETH_1y_cmc","NEAR_1y_cmc","BTC","ETH","NEAR","XRP","LTC","SOL","BONK","ADA"]
}
```

### Running the Web Server with Docker

1. Build the Docker image:
```bash
docker build -t yield-calculator .
```
2. Run the Docker container:
```bash
docker run -d -p 8080:8080 yield-calculator
```


### Example API Request

Use the following curl command to make a request to the API:
```bash
curl -X POST "http://localhost:8080/calculate_yield" -H "Content-Type: application/json" -d '{"price_csv": "BTC_1y_cmc", "num_loans_per_day": 5, "avg_initial_collateral_ratio": 1.5, "min_collateral_ratio": 1.2, "origination_fee_pct": 0.01, "liquidation_spread_pct": 0.70, "avg_repayment_days": 300, "avg_slippage_pct": 0.02, "avg_loan_amount": 1000}'
```
will return
```json
{
  "yield_percentage": 5.645147234051933,
  "start_datetime": "2023-09-12T00:00:00.000Z",
  "end_datetime": "2024-09-11T00:00:00.000Z",
  "parameters": {
    "price_csv": "Bitcoin_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv",
    "num_loans_per_day": 5,
    "avg_initial_collateral_ratio": 1.5,
    "min_collateral_ratio": 1.2,
    "origination_fee_pct": 0.01,
    "liquidation_spread_pct": 0.7,
    "avg_repayment_days": 300,
    "avg_slippage_pct": 0.02,
    "avg_loan_amount": 1000
  }
}
```


## Parameters

The tool will prompt you for the following parameters:

1. **Collateral Currency**: Choose between Bitcoin, Ethereum, or NEAR Protocol.
   - This determines which historical price data will be used for calculations.

2. **Number of loans per day**: The number of new loans issued each day in the simulation.
   - Default: 5

3. **Average initial collateral ratio**: The mean ratio of collateral value to loan value at loan origination.
   - Default: 1.5 (150% collateralization)
   - Note: Actual collateral ratios will vary around this average due to the normal distribution.

4. **Minimum collateral ratio**: The threshold below which a loan is liquidated.
   - Default: 1.2 (120% collateralization)

5. **Origination fee percentage**: The fee charged when a new loan is issued that goes to the lender as a form of yield, as a decimal.
   - Default: 0.01 (1%)

6. **Liquidation spread percentage**: The percentage of the loan that goes to the lender as a form of yield during liquidation, as a decimal.
   - Default: 0.70 (70%)

7. **Average repayment days**: The mean duration of loans before repayment.
   - Default: 300 days

8. **Average slippage percentage**: The expected price slippage during liquidation, as a decimal.
   - Default: 0.02 (2%)

9. **Average loan amount**: The mean amount for loans. Individual loan amounts are sampled from a lognormal distribution with this mean.
   - Default: 1000 (in the base currency, e.g., USD)
   - Note: Actual loan amounts will vary around this average due to the normal distribution.

## Output

The script will output the calculated historical yield as a percentage based on the input parameters and historical price data.

## Notes
### Assumptions
- The initial collateral ratio follows a normal distribution.
- The loan repayment duration based on borrower behavior follows a normal distribution.
- The liquidation happens at the low of the day (since we don't have intraday data currently). This means that the yield is underestimated.

### Historical Price Data
The historical price data is stored in the `data` directory and is taken from coinmarketcap and kraken (note the kraken data was originally in OHLCV format, which is converted to a price csv in the `convert_utc_to_timestamp.py` script and the data stops either at the beginning of 2024 or end of Q1 2024):
- Bitcoin_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv
- Ethereum_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv
- NEAR_Protocol_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv
- converted_BTCUSD_Daily_OHLCV.csv
- converted_ETHUSD_1440.csv
- converted_NEARUSD_1440.csv
- converted_XRPUSD_1440.csv
- converted_LTCUSD_1440.csv
- converted_SOLUSD_1440.csv
- converted_BONKUSD_1440.csv
- converted_ADAUSD_1440.csv


## TODO
- [ ] connect to frontend
- [x] Add more currencies
- [x] Add more historical data
- [ ] standardize the data format for all coins and ensure they all go up to the same timestamp
- [x] refactor csv data into a data directory
