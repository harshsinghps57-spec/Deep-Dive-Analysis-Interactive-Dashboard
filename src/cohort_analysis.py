import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File configuration
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Deep-Dive-Analysis-Interactive-Dashboard"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def run_cohort_analysis():
    print("Loading cleaned dataset for cohort analysis...")
    df = pd.read_csv(DATA_FILE)
    
    # 1. Standardize columns
    df.rename(columns={
        "Sales": "sales",
        "Profit": "profit",
        "Order Date": "order_date",
        "Customer ID": "customer_id"
    }, inplace=True)
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    # Extract order year-quarter (e.g., '2014Q1')
    df["order_quarter"] = df["order_date"].dt.to_period("Q")
    
    # 2. Determine first purchase quarter per customer (Cohort)
    cohorts = df.groupby("customer_id")["order_quarter"].min().reset_index()
    cohorts.rename(columns={"order_quarter": "cohort_quarter"}, inplace=True)
    
    # Merge back
    df = df.merge(cohorts, on="customer_id", how="left")
    
    # 3. Calculate Cohort Index (quarters since first purchase)
    # Convert Period to integer representations of quarters
    df["cohort_q_num"] = df["cohort_quarter"].astype(int)
    df["order_q_num"] = df["order_quarter"].astype(int)
    df["cohort_index"] = df["order_q_num"] - df["cohort_q_num"]
    
    # 4. Cohort Retention Matrix
    # Group by cohort_quarter and cohort_index, count unique customer IDs
    cohort_data = df.groupby(["cohort_quarter", "cohort_index"])["customer_id"].nunique().reset_index()
    
    # Pivot to create retention matrix
    retention_matrix = cohort_data.pivot(index="cohort_quarter", columns="cohort_index", values="customer_id")
    
    # Cohort Size (active users in index 0)
    cohort_sizes = retention_matrix.iloc[:, 0]
    
    # Divide row by cohort size to get percentage
    retention_rate = retention_matrix.divide(cohort_sizes, axis=0) * 100
    
    # Save retention rate data to CSV for dashboard
    retention_rate.to_csv(os.path.join(OUTPUT_DIR, "cohort_retention_rate.csv"))
    
    # 5. Cohort LTV Matrix (Cumulative sales per cohort customer)
    # Calculate revenue grouped by cohort and index
    cohort_revenue = df.groupby(["cohort_quarter", "cohort_index"])["sales"].sum().reset_index()
    revenue_matrix = cohort_revenue.pivot(index="cohort_quarter", columns="cohort_index", values="sales").fillna(0)
    
    # Calculate cumulative revenue
    cum_revenue = revenue_matrix.cumsum(axis=1)
    
    # Divide cumulative revenue by cohort size to get cumulative spend per customer (LTV)
    ltv_matrix = cum_revenue.divide(cohort_sizes, axis=0)
    ltv_matrix.to_csv(os.path.join(OUTPUT_DIR, "cohort_ltv.csv"))
    
    # 6. Visualizations
    print("Generating Cohort Retention Heatmap...")
    # Clean up index names for labels
    retention_rate.index = retention_rate.index.astype(str)
    ltv_matrix.index = ltv_matrix.index.astype(str)
    
    # Exclude recent cohorts for plotting if they don't have enough history,
    # but we will keep all and just mask NaNs.
    plt.figure(figsize=(14, 10))
    sns.heatmap(retention_rate, annot=True, fmt=".1f", cmap="YlGnBu", 
                mask=retention_rate.isnull(), cbar_kws={'label': 'Retention Rate (%)'})
    plt.title("Cohort Retention Analysis — Quarterly Customer Retention Rate (%)", fontsize=15, fontweight="bold")
    plt.xlabel("Cohort Index (Quarters after First Purchase)")
    plt.ylabel("Cohort Start (Quarter)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "cohort_retention_heatmap.png"), dpi=150)
    plt.close()
    
    print("Generating Cohort LTV Growth Line Chart...")
    plt.figure(figsize=(12, 7))
    # Plot top cohorts to keep line chart readable (e.g. cohorts starting in 2014)
    cohorts_2014 = [c for c in ltv_matrix.index if c.startswith("2014")]
    
    for cohort in cohorts_2014:
        # Drop NaN values for line chart
        values = ltv_matrix.loc[cohort].dropna()
        plt.plot(values.index, values.values, marker="o", linewidth=2.5, label=f"Cohort {cohort} (Size: {int(cohort_sizes.loc[pd.Period(cohort, freq='Q')]):,})")
        
    plt.title("Quarterly Cohort Customer Lifetime Value (LTV) Growth", fontsize=14, fontweight="bold")
    plt.xlabel("Quarters since First Purchase (Cohort Index)")
    plt.ylabel("Cumulative Spending per Customer ($)")
    plt.legend(title="Cohort Group")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "cohort_ltv_growth.png"), dpi=150)
    plt.close()
    
    print("Cohort analysis completed successfully.")

if __name__ == "__main__":
    run_cohort_analysis()
