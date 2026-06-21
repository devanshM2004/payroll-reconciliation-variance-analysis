# Payroll Reconciliation and Variance Analysis Model

A simple, transparent Python model that reconciles payroll for a pay period,
calculates net pay, and performs **period-over-period variance analysis** to
flag records that need review. Built with Python and pandas.

This project is intended as a portfolio piece for **entry-level banking,
credit, risk, financial operations, underwriting, and business analytics**
roles. It demonstrates the kind of structured, controls-minded reporting that
finance teams rely on every day.

---

## Why this matters in banking and finance

Reconciliation and variance analysis are core finance operations tasks. This
project shows hands-on ability in:

- **Payroll reconciliation** – recalculating pay from source inputs (hours,
  rates, deductions) rather than trusting a single reported figure.
- **Variance analysis** – comparing current-period results against a prior
  period to measure change in both dollars and percentage terms.
- **Exception flagging** – automatically surfacing records that move more than
  a defined tolerance (10.00%) so analysts can focus on what matters.
- **Finance operations reporting** – producing a clean, auditable CSV output
  that could be handed to a reviewer or loaded into another system.
- **Internal control review** – applying a consistent, repeatable rule set so
  results are explainable and defensible, the foundation of any control.

These are the same habits used in credit review, risk monitoring,
underwriting checks, and month-end financial close.

---

## What the model calculates

For each employee in the pay period:

| Calculation | Rule |
|---|---|
| Regular pay | `regular_hours × hourly_rate` |
| Overtime pay | `overtime_hours × hourly_rate × 1.5` |
| Gross pay | `regular pay + overtime pay` |
| Deductions | `gross pay × deduction_rate` |
| Net pay | `gross pay − deductions` |
| Dollar variance | `current net pay − prior net pay` |
| Percent variance | `(dollar variance ÷ prior net pay) × 100` |
| Exception flag | `TRUE` when `|percent variance| > 10.00%` |

---

## Project structure

```
.
├── README.md                     # Project overview (this file)
├── requirements.txt              # Python dependencies
├── main.py                       # Entry point: load, calculate, report
├── data/
│   └── sample_payroll_data.csv   # Sample input payroll data
├── output/
│   └── payroll_output.csv        # Generated reconciliation report
└── src/
    └── calculate_payroll.py      # Reusable payroll & variance logic
```

---

## How to run

1. (Optional) create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the model from the project root:

   ```bash
   python main.py
   ```

The script prints a short exception summary to the console and writes the full
report to `output/payroll_output.csv`.

---

## Output

`output/payroll_output.csv` contains every input field plus the calculated
columns: `regular_pay`, `overtime_pay`, `gross_pay`, `deductions`, `net_pay`,
`dollar_variance`, `percent_variance`, and `variance_flag`.

Records where the absolute percentage variance exceeds **10.00%** are flagged
(`variance_flag = True`) as reconciliation exceptions for analyst review.

---

## Design notes

- **Kept intentionally simple** – plain pandas, clear functions, and inline
  documentation so the logic is easy to follow and discuss in an interview.
- **Separation of concerns** – calculation logic lives in
  `src/calculate_payroll.py`; `main.py` only handles input/output.
- **No web app, no machine learning** – the focus is correct, explainable
  finance calculations and clean reporting.
