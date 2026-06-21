"""
Payroll calculation and variance analysis logic.

This module contains the core, reusable functions for the
Payroll Reconciliation and Variance Analysis Model. Keeping the
calculations here (separate from main.py) makes the logic easy to
read, test, and reason about during an interview or code review.

Calculation rules
-----------------
- Regular pay     = regular_hours * hourly_rate
- Overtime pay    = overtime_hours * hourly_rate * OVERTIME_MULTIPLIER
- Gross pay       = regular pay + overtime pay
- Deductions      = gross pay * deduction_rate
- Net pay         = gross pay - deductions
- Dollar variance = current net pay - prior net pay
- Percent variance= (dollar variance / prior net pay) * 100
- Exception flag  = TRUE when |percent variance| > VARIANCE_THRESHOLD
"""

import pandas as pd

# Overtime is paid at 1.5x the standard hourly rate (time-and-a-half).
OVERTIME_MULTIPLIER = 1.5

# Records whose absolute net-pay variance exceeds this percentage are
# flagged for review as reconciliation exceptions.
VARIANCE_THRESHOLD = 10.00


def calculate_regular_pay(regular_hours, hourly_rate):
    """Return standard pay for hours worked at the base rate."""
    return regular_hours * hourly_rate


def calculate_overtime_pay(overtime_hours, hourly_rate):
    """Return overtime pay (time-and-a-half on the base rate)."""
    return overtime_hours * hourly_rate * OVERTIME_MULTIPLIER


def calculate_gross_pay(regular_pay, overtime_pay):
    """Return gross pay (regular pay plus overtime pay)."""
    return regular_pay + overtime_pay


def calculate_deductions(gross_pay, deduction_rate):
    """Return total deductions (taxes, benefits, etc.) on gross pay."""
    return gross_pay * deduction_rate


def calculate_net_pay(gross_pay, deductions):
    """Return net (take-home) pay after deductions."""
    return gross_pay - deductions


def calculate_dollar_variance(current_net_pay, prior_net_pay):
    """Return the dollar change in net pay versus the prior period."""
    return current_net_pay - prior_net_pay


def calculate_percent_variance(dollar_variance, prior_net_pay):
    """Return the percentage change in net pay versus the prior period.

    Guards against division by zero when there is no prior-period pay.
    """
    return dollar_variance.divide(prior_net_pay).where(prior_net_pay != 0) * 100


def flag_variance(percent_variance, threshold=VARIANCE_THRESHOLD):
    """Return True where the absolute percentage variance exceeds threshold."""
    return percent_variance.abs() > threshold


def process_payroll(df):
    """Run the full payroll and variance calculation on a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain the columns: regular_hours, overtime_hours,
        hourly_rate, deduction_rate, prior_net_pay.

    Returns
    -------
    pandas.DataFrame
        A copy of the input with all calculated payroll, variance, and
        exception-flag columns added, rounded to two decimal places.
    """
    df = df.copy()

    df["regular_pay"] = calculate_regular_pay(df["regular_hours"], df["hourly_rate"])
    df["overtime_pay"] = calculate_overtime_pay(df["overtime_hours"], df["hourly_rate"])
    df["gross_pay"] = calculate_gross_pay(df["regular_pay"], df["overtime_pay"])
    df["deductions"] = calculate_deductions(df["gross_pay"], df["deduction_rate"])
    df["net_pay"] = calculate_net_pay(df["gross_pay"], df["deductions"])

    df["dollar_variance"] = calculate_dollar_variance(
        df["net_pay"], df["prior_net_pay"]
    )
    df["percent_variance"] = calculate_percent_variance(
        df["dollar_variance"], df["prior_net_pay"]
    )
    df["variance_flag"] = flag_variance(df["percent_variance"])

    # Round all monetary and percentage columns for a clean report.
    money_cols = [
        "regular_pay",
        "overtime_pay",
        "gross_pay",
        "deductions",
        "net_pay",
        "dollar_variance",
        "percent_variance",
    ]
    df[money_cols] = df[money_cols].round(2)

    return df
