import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_yield(
    price_csv,
    num_loans_per_day,
    avg_initial_collateral_ratio,
    min_collateral_ratio,
    origination_fee_pct,
    liquidation_spread_pct,
    avg_repayment_days,
    avg_slippage_pct,
    avg_loan_amount
):
    # Read historical price data
    df = pd.read_csv(price_csv, parse_dates=['timeOpen'])
    df.set_index('timeOpen', inplace=True)
    df.sort_index(inplace=True)

    # Initialize variables
    loans = []
    total_yield = 0
    total_loaned = 0

    # Simulate loans and liquidations
    for date, row in df.iterrows():
        price = row['low']

        # Generate new loans
        for _ in range(num_loans_per_day):
            # Sample loan amount from normal distribution
            loan_amount = np.random.normal(avg_loan_amount, avg_loan_amount/2)
            
            initial_collateral_ratio = max(np.random.normal(avg_initial_collateral_ratio, avg_initial_collateral_ratio/4), min_collateral_ratio + 0.05)
            collateral_amount = loan_amount * initial_collateral_ratio / price
            loan = {
                'timestamp': date,
                'amount': loan_amount,
                'collateral': collateral_amount,
                'liquidation_price': loan_amount * min_collateral_ratio / collateral_amount,
                'repayment_date': date + timedelta(days=np.random.normal(avg_repayment_days, avg_repayment_days/4))
            }
            loans.append(loan)
            total_loaned += loan_amount
            total_yield += loan_amount * origination_fee_pct

        # Update collateral ratio for each loan
        for loan in loans:
            loan['current_collateral_ratio'] = (loan['collateral'] * price) / loan['amount']

        # Check for liquidations and repayments
        loans_to_remove = []
        for loan in loans:
            if loan['current_collateral_ratio'] <= min_collateral_ratio:
                # Liquidation
                recovered_amount = loan['collateral'] * price * (1 - avg_slippage_pct)
                liquidation_yield = min(recovered_amount - loan['amount'], loan['amount'] * liquidation_spread_pct)
                print(f"Liquidation yield: {liquidation_yield}")
                total_yield += liquidation_yield
                loans_to_remove.append(loan)
            elif date >= loan['repayment_date']:
                # Repayment
                loans_to_remove.append(loan)

        # Remove liquidated and repaid loans
        for loan in loans_to_remove:
            loans.remove(loan)

    # Calculate yield as a percentage of total loaned amount
    yield_percentage = (total_yield / total_loaned) * 100

    return yield_percentage

def get_user_input():
    print("Please enter the following parameters:")
    
    price_csv = input("Cryptocurrency (BTC, ETH, or NEAR) [default: BTC]: ").strip() or "BTC"
    while price_csv not in ["BTC", "ETH", "NEAR"]:
        price_csv = input("Invalid choice. Please enter BTC, ETH, or NEAR: ").strip()

    params = {
        "num_loans_per_day": int(input("Number of loans per day [default: 5]: ") or 5),
        "avg_initial_collateral_ratio": float(input("Average initial collateral ratio [default: 1.5]: ") or 1.5),
        "min_collateral_ratio": float(input("Minimum collateral ratio [default: 1.2]: ") or 1.2),
        "origination_fee_pct": float(input("Origination fee percentage [default: 0.01]: ") or 0.01),
        "liquidation_spread_pct": float(input("Liquidation spread percentage [default: 0.70]: ") or 0.70),
        "avg_repayment_days": int(input("Average repayment days [default: 300]: ") or 300),
        "avg_slippage_pct": float(input("Average slippage percentage [default: 0.02]: ") or 0.02),
        "avg_loan_amount": float(input("Average loan amount [default: 1000]: ") or 1000)
    }

    return price_csv, params

if __name__ == "__main__":
    csv_files = {
        'BTC': 'Bitcoin_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv',
        'ETH': 'Ethereum_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv',
        'NEAR': 'NEAR Protocol_9_12_2023-9_11_2024_historical_data_coinmarketcap.csv'
    }

    price_csv, params = get_user_input()
    price_csv = csv_files[price_csv]

    yield_pct = calculate_yield(price_csv, **params)

    print(f"\nHistorical yield for {price_csv}: {yield_pct:.2f}%")
