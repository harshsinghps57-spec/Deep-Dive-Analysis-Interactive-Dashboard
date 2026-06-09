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

def run_rfm_analysis():
    print("Loading cleaned dataset for RFM analysis...")
    df = pd.read_csv(DATA_FILE)
    
    # Standardize column names
    df.rename(columns={
        "Sales": "sales",
        "Profit": "profit",
        "Order Date": "order_date",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "customer_segment", # segment is customer segment (Consumer/Corporate)
        "Order ID": "order_id"
    }, inplace=True)
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    # 1. Calculate RFM Raw Metrics
    # Max date in dataset + 1 day for reference
    max_date = df["order_date"].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby("customer_id").agg({
        "order_date": lambda x: (max_date - x.max()).days, # Recency
        "order_id": "nunique",                            # Frequency
        "sales": "sum",                                    # Monetary
        "customer_name": "first",
        "customer_segment": "first"
    }).reset_index()
    
    rfm.rename(columns={
        "order_date": "recency",
        "order_id": "frequency",
        "sales": "monetary"
    }, inplace=True)
    
    # 2. Compute RFM Scores (1 to 5, where 5 is best)
    # Using rank method first to avoid duplicate bin edge issues in qcut
    rfm["R_score"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int) # Lower recency is better
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int) # Higher frequency is better
    rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int) # Higher monetary is better
    
    # 3. Define Customer Segment Business Rules
    def segment_customer(row):
        r, f, m = row["R_score"], row["F_score"], row["M_score"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 3 and m >= 3:
            return "Loyalists"
        elif r >= 3 and f <= 2:
            return "Potential Loyalists"
        elif r <= 2 and (f >= 3 or m >= 3):
            return "At Risk"
        else:
            return "Hibernating"
            
    rfm["rfm_segment"] = rfm.apply(segment_customer, axis=1)
    
    # Save RFM Customer segments list
    rfm_csv_path = os.path.join(OUTPUT_DIR, "rfm_customer_segments.csv")
    rfm.to_csv(rfm_csv_path, index=False)
    print(f"RFM analysis completed and saved to {rfm_csv_path}")
    
    # 4. Segment Summary Dataframe
    segment_summary = rfm.groupby("rfm_segment").agg(
        customer_count=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        total_revenue=("monetary", "sum"),
        avg_revenue=("monetary", "mean")
    ).reset_index()
    
    # Compute share percentages
    total_customers = len(rfm)
    total_rev = rfm["monetary"].sum()
    segment_summary["customer_share_%"] = (segment_summary["customer_count"] / total_customers * 100).round(2)
    segment_summary["revenue_share_%"] = (segment_summary["total_revenue"] / total_rev * 100).round(2)
    
    segment_summary.to_csv(os.path.join(OUTPUT_DIR, "rfm_segment_summary.csv"), index=False)
    
    # 5. Visualizations
    # Chart 1: Segment Distribution (Size & Count)
    plt.figure(figsize=(10, 6))
    seg_order = rfm["rfm_segment"].value_counts().index
    sns.countplot(data=rfm, x="rfm_segment", order=seg_order, palette="viridis")
    plt.title("Distribution of Customer Segments (RFM)", fontsize=14, fontweight="bold")
    plt.xlabel("Customer Segment")
    plt.ylabel("Number of Customers")
    # Add values on top of bars
    ax = plt.gca()
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2., p.get_height() + 5),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='semibold')
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "rfm_segment_distribution.png"), dpi=150)
    plt.close()
    
    # Chart 2: Customer Share vs Revenue Share (Grouped Bar Chart)
    melted = pd.melt(segment_summary, id_vars="rfm_segment", value_vars=["customer_share_%", "revenue_share_%"])
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=melted, x="rfm_segment", y="value", hue="variable", palette="Set2")
    plt.title("Customer Share vs. Revenue Share per RFM Segment", fontsize=14, fontweight="bold")
    plt.xlabel("RFM Segment")
    plt.ylabel("Percentage Share (%)")
    plt.legend(title="Metric Share", labels=["Customer Share %", "Revenue Share %"])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "rfm_share_comparison.png"), dpi=150)
    plt.close()
    
    # Chart 3: Scatter Plot of Recency vs. Frequency, colored by Segment
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=rfm, x="recency", y="frequency", hue="rfm_segment", alpha=0.8, palette="Set1", s=60)
    plt.title("RFM Mapping — Customer Recency vs. Frequency Scatter Plot", fontsize=14, fontweight="bold")
    plt.xlabel("Recency (Days since Last Purchase)")
    plt.ylabel("Frequency (Total Number of Orders)")
    plt.legend(title="Customer Segment")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "rfm_recency_vs_frequency.png"), dpi=150)
    plt.close()
    
    print("RFM charts generated successfully.")

if __name__ == "__main__":
    run_rfm_analysis()
