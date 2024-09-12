from calculate_yield import calculate_yield
from CSV_FILES import CSV_FILES

def get_user_input():
    print("Please enter the following parameters:")
    
    price_csv = input("Cryptocurrency (BTC_1y_cmc, ETH_1y_cmc, NEAR_1y_cmc, BTC, ETH, NEAR, XRP, LTC, SOL, BONK, ADA) [default: BTC_1y_cmc]: ").strip() or "BTC_1y_cmc"
    while price_csv not in ["BTC_1y_cmc", "ETH_1y_cmc", "NEAR_1y_cmc", "BTC", "ETH", "NEAR", "XRP", "LTC", "SOL", "BONK", "ADA"]:
        price_csv = input("Invalid choice. Please enter BTC_1y_cmc, ETH_1y_cmc, NEAR_1y_cmc, BTC, ETH, NEAR, XRP, LTC, SOL, BONK, ADA: ").strip()

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
    price_csv, params = get_user_input()
    price_csv = CSV_FILES[price_csv]

    print(calculate_yield(price_csv, **params))