import numpy as np
import pandas as pd
from datetime import timedelta


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
    df = pd.read_csv(price_csv, parse_dates=['time'])
    df.set_index('time', inplace=True)
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
            # Sample loan amount from normal distribution with mean avg_loan_amount and std dev of avg_loan_amount/2
            loan_amount = np.random.normal(avg_loan_amount, avg_loan_amount/2)

            initial_collateral_ratio = max(np.random.normal(avg_initial_collateral_ratio, avg_initial_collateral_ratio/4), min_collateral_ratio + 0.05)
            collateral_amount = loan_amount * initial_collateral_ratio / price
            loan = {
                'timestamp': date,
                'amount': loan_amount,
                'collateral': collateral_amount,
                'liquidation_price': loan_amount * min_collateral_ratio / collateral_amount,
                # Sample repayment date from normal distribution around avg_repayment_days with std dev of avg_repayment_days/4
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
                # print(f"Liquidation yield: {liquidation_yield}")
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