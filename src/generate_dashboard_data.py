import os
import json
import pandas as pd
import numpy as np

# File configuration
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Deep-Dive-Analysis-Interactive-Dashboard"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
RFM_FILE = os.path.join(BASE_DIR, "output", "rfm_customer_segments.csv")
RETENTION_FILE = os.path.join(BASE_DIR, "output", "cohort_retention_rate.csv")
LTV_FILE = os.path.join(BASE_DIR, "output", "cohort_ltv.csv")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
DATA_JS_FILE = os.path.join(DASHBOARD_DIR, "data.js")

os.makedirs(DASHBOARD_DIR, exist_ok=True)

def generate_data():
    print("Generating dashboard dataset...")
    df = pd.read_csv(DATA_FILE)
    rfm = pd.read_csv(RFM_FILE)
    retention = pd.read_csv(RETENTION_FILE)
    ltv = pd.read_csv(LTV_FILE)
    
    # 1. Base KPIs
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    aov = float(df.groupby("Order ID")["Sales"].sum().mean())
    
    # Purchase frequency: orders per customer
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()
    purchase_frequency = float(total_orders / total_customers)
    
    # Overall average retention: percentage of returning customers
    # (customers with >1 order)
    returning_customers = rfm[rfm["frequency"] > 1]["customer_id"].nunique()
    overall_retention_rate = float(returning_customers / total_customers * 100)
    
    kpis = {
        "sales": round(total_sales, 2),
        "profit": round(total_profit, 2),
        "aov": round(aov, 2),
        "purchase_frequency": round(purchase_frequency, 2),
        "total_customers": total_customers,
        "overall_retention": round(overall_retention_rate, 2)
    }
    
    # 2. Cohort Retention Heatmap Data
    retention.rename(columns={retention.columns[0]: "cohort"}, inplace=True)
    cohort_labels = retention["cohort"].astype(str).tolist()
    
    # Structure matrix as a list of rows
    # Convert NaNs to null for JSON compatibility
    retention_matrix = []
    for idx, row in retention.iterrows():
        row_vals = []
        for col in retention.columns[1:]:
            val = row[col]
            row_vals.append(None if pd.isna(val) else round(float(val), 1))
        retention_matrix.append({
            "cohort": str(row["cohort"]),
            "values": row_vals
        })
        
    # 3. Cohort LTV Growth Data
    ltv.rename(columns={ltv.columns[0]: "cohort"}, inplace=True)
    ltv_matrix = []
    for idx, row in ltv.iterrows():
        row_vals = []
        for col in ltv.columns[1:]:
            val = row[col]
            row_vals.append(None if pd.isna(val) else round(float(val), 2))
        ltv_matrix.append({
            "cohort": str(row["cohort"]),
            "values": row_vals
        })
        
    # 4. RFM Segmentation Data
    # Customer counts, average recency, average frequency, total monetary per segment
    summary = rfm.groupby("rfm_segment").agg(
        count=("customer_id", "count"),
        recency=("recency", "mean"),
        frequency=("frequency", "mean"),
        monetary=("monetary", "sum")
    ).reset_index()
    
    rfm_segments = {}
    for idx, row in summary.iterrows():
        seg_name = row["rfm_segment"]
        rfm_segments[seg_name] = {
            "count": int(row["count"]),
            "recency": round(float(row["recency"]), 1),
            "frequency": round(float(row["frequency"]), 2),
            "monetary": round(float(row["monetary"]), 2)
        }
        
    # 5. Top customers in each segment for explorer
    # Select top 5 customers per segment by monetary spend
    top_customers = {}
    for seg in rfm["rfm_segment"].unique():
        seg_customers = rfm[rfm["rfm_segment"] == seg].sort_values("monetary", ascending=False).head(5)
        top_customers[seg] = []
        for idx, row in seg_customers.iterrows():
            top_customers[seg].append({
                "id": str(row["customer_id"]),
                "name": str(row["customer_name"]),
                "recency": int(row["recency"]),
                "frequency": int(row["frequency"]),
                "monetary": round(float(row["monetary"]), 2),
                "segment": str(row["customer_segment"])
            })
            
    # Combine everything
    dashboard_payload = {
        "kpis": kpis,
        "cohorts": {
            "labels": cohort_labels,
            "retention": retention_matrix,
            "ltv": ltv_matrix
        },
        "rfm": {
            "summary": rfm_segments,
            "top_customers": top_customers
        }
    }
    
    # Save to data.js
    with open(DATA_JS_FILE, "w", encoding="utf-8") as f:
        f.write("// Pre-calculated data generated from Superstore dataset for Week 3 BI Dashboard\n")
        f.write("const week3Data = ")
        json.dump(dashboard_payload, f, indent=2)
        f.write(";\n")
        
    print(f"Dashboard data generated and written to {DATA_JS_FILE}")

if __name__ == "__main__":
    generate_data()
