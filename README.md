# Synthetic Sales Data Generator

A Python program that generates realistic, fake sales transaction data for testing and demos, then builds a second dataset that statistically matches the first.

Built for a scenario where a client's legal team blocked the use of real transaction data during a demo phase, so realistic synthetic data was needed instead.

## What it does

1. **Generates** an original dataset of 50 to 50,000 sales transactions with 10 fields each.
2. **Analyzes** the distribution of every field (counts and percentages).
3. **Builds weighted sampling pools** from those distributions.
4. **Generates a second dataset** that reproduces the first dataset's profile.
5. **Validates** the result with a side-by-side comparison report.

In testing with 25,000 and 20,000 records, most fields in the two datasets matched within 1 to 2 percentage points.

## Dataset fields

| Field | Description |
|---|---|
| TransactionID | Unique ID for each sale |
| Region | North, South, East, West, Central |
| CustomerType | Retail, Wholesale, Government, Education, Nonprofit |
| ProductCategory | Office Supplies, Technology, Furniture, Maintenance, Food Service |
| SalesChannel | Online, In Person, Phone, Partner |
| UnitsSold | 1 to 100 |
| UnitPrice | $5.00 to $2,500.00 |
| DiscountApplied | Yes or No (5% to 25% off when Yes) |
| PurchaseTotal | Units × price, minus any discount |
| RiskFlag | Low (under $1,000), Medium (under $10,000), High |

## How to run

Requires Python 3 (no extra libraries).

```
python sales_data_generator.py
```

Keep `business_lists.txt` in the same folder. The program asks how many records to create, then writes `business_data.csv` and `business_data_set_2.csv`.

## Files

- `sales_data_generator.py`: the program
- `business_lists.txt`: the regions, customer types, categories, and channels it draws from
- `business_data.csv`: sample output, original dataset (4,899 records)
- `business_data_set_2.csv`: sample output, second dataset built from the first (2,500 records)

## Skills shown

Python, file input/output, input validation, data generation, frequency analysis, weighted sampling, and data validation reporting.

## Author

Ashton Oliphant, B.B.A. Computer Information Systems, Texas State University
