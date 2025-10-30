import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("superstore.csv", encoding="latin1")

# Convert Order Date to a datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Create a monthly column for grouping
df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()

# Group and sum monthly sales
monthly_sales = df.groupby("Order Month")["Sales"].sum()

# Plot
plt.figure(figsize=(12,5))
plt.plot(monthly_sales.index, monthly_sales.values, linewidth=2)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.grid(True)

plt.show()
