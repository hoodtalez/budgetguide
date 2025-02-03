#!/usr/bin/env python3
"""
BudgetEditor
============
A tool to process a CSV file of financial transactions by:

  • Removing Centrelink payments.
  • Removing transactions that match “bad” keywords.
  • Adding (or replacing) the income with a full-time employment income.
  • Producing a summary report that shows:
      - Revised total income and expenses.
      - Net balance.
      - A recommended spending breakdown (using the 50/30/20 rule).

Usage:
  python budget_editor.py --input input.csv --output output.csv --income 4000 \
       [--bad_keywords "bad,fraud,error"]

The CSV is expected to have at least the following columns:
  Date, Description, Amount

Transactions with positive Amounts are incomes; negative are expenses.
"""

import argparse
import logging
import sys
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("BudgetEditor")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process a CSV of financial transactions to remove Centrelink and bad payments, "
                    "inject a full-time income row, and produce a balanced budget summary."
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the input CSV file of transactions."
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Path to the output CSV file with revised transactions."
    )
    parser.add_argument(
        "--income", "-I", type=float, required=True,
        help="Full-time employment income (e.g., monthly or per period)."
    )
    parser.add_argument(
        "--bad_keywords", "-b", default="bad,fraud,error",
        help="Comma-separated list of keywords for transactions to remove as bad."
    )
    parser.add_argument(
        "--centrelink_keyword", "-c", default="Centrelink",
        help="Keyword to filter out Centrelink payments."
    )
    return parser.parse_args()


def load_transactions(input_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(input_path)
        # Ensure required columns exist.
        for col in ["Date", "Description", "Amount"]:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                sys.exit(1)
        return df
    except Exception as e:
        logger.error(f"Failed to read CSV file {input_path}: {e}")
        sys.exit(1)


def filter_transactions(df: pd.DataFrame, centrelink_keyword: str, bad_keywords: list) -> pd.DataFrame:
    # Remove Centrelink payments.
    before = len(df)
    df = df[~df["Description"].str.contains(centrelink_keyword, case=False, na=False)]
    logger.info(f"Removed {before - len(df)} Centrelink transactions.")

    # Remove transactions whose Description contains any bad keyword.
    mask_bad = df["Description"].str.contains("|".join(bad_keywords), case=False, na=False)
    before = len(df)
    df = df[~mask_bad]
    logger.info(f"Removed {before - len(df)} transactions matching bad keywords: {bad_keywords}")

    return df


def add_employment_income(df: pd.DataFrame, income: float) -> pd.DataFrame:
    # Check if there is already an "Employment Income" row.
    if not df["Description"].str.contains("Employment Income", case=False, na=False).any():
        # Create a new row for Employment Income.
        new_row = {"Date": pd.NaT, "Description": "Employment Income", "Amount": income}
        df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
        logger.info("Added Employment Income row.")
    else:
        logger.info("Employment Income row already exists; skipping addition.")
    return df


def compute_summary(df: pd.DataFrame, full_income: float) -> dict:
    # Sum incomes (Amount > 0) and expenses (Amount < 0)
    total_income = df[df["Amount"] > 0]["Amount"].sum()
    total_expenses = df[df["Amount"] < 0]["Amount"].sum()
    balance = total_income + total_expenses  # expenses are negative

    # For the purpose of a balanced guide, use the full_time income (provided by user)
    # Recommended allocations using 50/30/20 rule:
    needs = full_income * 0.50
    wants = full_income * 0.30
    savings = full_income * 0.20

    summary = {
        "full_time_income": full_income,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "recommended": {
            "needs": needs,
            "wants": wants,
            "savings": savings
        }
    }
    return summary


def main():
    args = parse_args()
    bad_keywords = [word.strip() for word in args.bad_keywords.split(",")]

    # Load transactions.
    df = load_transactions(args.input)

    # Filter out Centrelink and bad transactions.
    df_filtered = filter_transactions(df, args.centrelink_keyword, bad_keywords)

    # Add employment income row if needed.
    df_final = add_employment_income(df_filtered, args.income)

    # Write the revised CSV.
    try:
        df_final.to_csv(args.output, index=False)
        logger.info(f"Revised transactions written to {args.output}")
    except Exception as e:
        logger.error(f"Failed to write CSV file {args.output}: {e}")
        sys.exit(1)

    # Compute and print the summary.
    summary = compute_summary(df_final, args.income)
    print("\nBudget Summary Report")
    print("=====================")
    print(f"Full-Time Income Provided: ${summary['full_time_income']:.2f}")
    print(f"Total Income (after filtering): ${summary['total_income']:.2f}")
    print(f"Total Expenses: ${summary['total_expenses']:.2f}")
    print(f"Balance: ${summary['balance']:.2f}")
    print("\nRecommended Spending (50/30/20):")
    print(f"  Needs:   ${summary['recommended']['needs']:.2f}")
    print(f"  Wants:   ${summary['recommended']['wants']:.2f}")
    print(f"  Savings: ${summary['recommended']['savings']:.2f}")


if __name__ == "__main__":
    main()
