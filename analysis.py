# Superstore analysis — pandas version
# Assumes analysis.py and superstore.csv are in the same folder.

import pandas as pd
from pathlib import Path

CSV = "superstore.csv"

# --- Load & clean ---
df = pd.read_csv(CSV, encoding="latin1")

# Standardize dtypes
for col in ["Sales", "Quantity", "Discount", "Profit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  errors="coerce")

# Quick sanity checks
assert df["Order Date"].notna().all(), "Order Date has nulls after parsing."
assert df["Sales"].notna().all(), "Sales has nulls after coercion."

# --- 1) Total sales by region ---
region_sales = (
    df.groupby("Region", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

# --- 2) Total sales by product category ---
category_sales = (
    df.groupby("Category", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

# --- 3) Top 10 customers by total purchase amount ---
top_customers = (
    df.groupby(["Customer ID", "Customer Name"], as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
      .head(10)
)

# --- 4) Monthly sales trend (group by month & year) ---
df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
monthly_sales = (
    df.groupby("Order Month", as_index=False)["Sales"]
      .sum()
      .sort_values("Order Month")
)

# --- 5) (Bonus) Profitability by category & sub-category ---
profitability = (
    df.groupby(["Category", "Sub-Category"], as_index=False)
      .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
      .assign(Profit_Margin=lambda d: (d["Profit"] / d["Sales"]).round(4))
      .sort_values(["Category","Profit_Margin"], ascending=[True, False])
)

# --- Save CSV outputs (so you can submit or visualize later) ---
outdir = Path(".") / "outputs"
outdir.mkdir(exist_ok=True)

region_sales.to_csv(outdir / "region_sales.csv", index=False)
category_sales.to_csv(outdir / "category_sales.csv", index=False)
top_customers.to_csv(outdir / "top_customers.csv", index=False)
monthly_sales.to_csv(outdir / "monthly_sales.csv", index=False)
profitability.to_csv(outdir / "profitability_by_category_subcategory.csv", index=False)

# --- Print concise summaries to terminal ---
print("\n=== Total Sales by Region ===")
print(region_sales)

print("\n=== Total Sales by Category ===")
print(category_sales)

print("\n=== Top 10 Customers by Sales ===")
print(top_customers)

print("\n=== Monthly Sales Trend (first 12 rows) ===")
print(monthly_sales.head(12))

print("\n=== Profitability by Category/Sub-Category (top 12 rows) ===")
print(profitability.head(12))

print("\nFiles written to ./outputs/")
