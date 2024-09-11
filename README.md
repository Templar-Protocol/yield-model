# Crypto Loan Yield Calculator

This tool calculates the historical yield for cryptocurrency loans based on various parameters.

## Usage

1. Ensure you have Python installed on your system.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the script:
   ```
   python main.py
   ```
4. Follow the interactive prompts to input parameters.

## Parameters

The tool will prompt you for the following parameters:

1. **Collateral Currency**: Choose between Bitcoin, Ethereum, or NEAR Protocol.
   - This determines which historical price data will be used for calculations.

2. **Number of loans per day**: The number of new loans issued each day in the simulation.
   - Default: 5

3. **Average initial collateral ratio**: The mean ratio of collateral value to loan value at loan origination.
   - Default: 1.5 (150% collateralization)

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

9. **Loan amount**: The principal amount for each loan.
   - Default: 1000 (in the base currency, e.g., USD)

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
