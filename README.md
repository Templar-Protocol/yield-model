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

### Running the Web Server

3. Start the FastAPI server:
    ```bash
    python3 main.py
    ```
   This will start the server on `http://localhost:8000`.

4. You can now send POST requests to the `/calculate_yield` endpoint to calculate yields.

The API will return a JSON object with the calculated historical yield as a percentage based on the input parameters and historical price data in the following format:
```json
{
    "yield_percentage":5.645147234051933
}
```


### Example API Request

Use the following curl command to make a request to the API:
```bash
curl -X POST "http://localhost:8000/calculate_yield" -H "Content-Type: application/json" -d '{"price_csv": "BTC", "num_loans_per_day": 5, "avg_initial_collateral_ratio": 1.5, "min_collateral_ratio": 1.2, "origination_fee_pct": 0.01, "liquidation_spread_pct": 0.70, "avg_repayment_days": 300, "avg_slippage_pct": 0.02, "avg_loan_amount": 1000}'
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
Ensure that you have the corresponding CSV files for historical price data in the same directory as the script:
- Bitcoin_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv
- Ethereum_historical_data.csv
- NEAR_Protocol_historical_data.csv


## TODO
- [ ] connect to frontend
- [ ] Add more currencies
- [ ] Add more historical data
- [ ] standardize the data format for all coins and ensure they all go up to the same timestamp
- [ ] refactor csv data into a data directory
