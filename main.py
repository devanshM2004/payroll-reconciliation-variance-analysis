"""
Payroll Reconciliation and Variance Analysis Model
==================================================

Entry point for the project. This script:

1. Loads the sample payroll data.
2. Calculates regular, overtime, gross, deduction, and net pay.
3. Compares current-period net pay against the prior period.
4. Computes dollar and percentage variances.
5. Flags records where the absolute variance exceeds 10.00%.
6. Writes a clean CSV report to output/payroll_output.csv.

Run from the project root:

    python main.py
"""

import os

import pandas as pd

from src.calculate_payroll import process_payroll, VARIANCE_THRESHOLD

INPUT_PATH = os.path.join("data", "sample_payroll_data.csv")
OUTPUT_PATH = os.path.join("output", "payroll_output.csv")


def main():
    # Load the source payroll data.
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} payroll records from {INPUT_PATH}")

    # Run all payroll and variance calculations.
    results = process_payroll(df)

    # Make sure the output directory exists, then write the report.
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote reconciliation report to {OUTPUT_PATH}")

    # Print a short summary of flagged exceptions for quick review.
    flagged = results[results["variance_flag"]]
    print(
        f"\nException summary: {len(flagged)} of {len(results)} records "
        f"exceed the {VARIANCE_THRESHOLD:.2f}% variance threshold."
    )
    if not flagged.empty:
        summary_cols = [
            "employee_id",
            "employee_name",
            "prior_net_pay",
            "net_pay",
            "dollar_variance",
            "percent_variance",
        ]
        print(flagged[summary_cols].to_string(index=False))


if __name__ == "__main__":
    main()
