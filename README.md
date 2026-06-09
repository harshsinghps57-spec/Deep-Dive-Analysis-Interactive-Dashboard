# 📊 Customer Deep-Dive & Interactive Dashboarding — Week 3 Internship Task

> **ApexPlanet Software Pvt. Ltd. | Internship Task 3 | Timeline: 12 Days**

---

## 📌 Project Overview

This repository contains the deliverables for the **Week 3 Internship Task: Deep-Dive Analysis & Interactive Dashboarding**. Grouping customer transactions from the Superstore dataset, we executed two detailed analytical deep-dives:
1. **Quarterly Cohort Retention & Lifetime Value (LTV) Analysis**: Grouping customers by their acquisition quarter and tracking retention decay and cumulative value trends over 12 quarters.
2. **RFM Customer Segmentation**: Calculating Recency, Frequency, and Monetary scores per customer to map them into actionable business segments (Champions, Loyalists, Potential Loyalists, At Risk, Hibernating).

---

## 📂 Repository Structure

```
Deep-Dive-Analysis-Interactive-Dashboard/
│
├── data/
│   ├── Sample - Superstore.csv       # Raw transaction dataset
│   └── cleaned_superstore.csv        # Prepared dataset (from Week 1)
│
├── src/
│   ├── cohort_analysis.py            # Cohort retention & LTV analysis engine
│   ├── rfm_analysis.py               # RFM customer segmentation engine
│   └── generate_dashboard_data.py    # Pre-aggregates calculations into JSON
│
├── output/
│   ├── cohort_retention_rate.csv     # Raw cohort retention percentages matrix
│   ├── cohort_ltv.csv                # Cumulative spend per cohort customer matrix
│   ├── rfm_customer_segments.csv     # List of all customers with their RFM scores & segments
│   ├── rfm_segment_summary.csv       # Financial summaries of RFM segments
│   ├── deep_dive_report.md           # Comprehensive deep-dive analytical report
│   └── charts/                       # Folder containing generated plots
│       ├── cohort_retention_heatmap.png
│       ├── cohort_ltv_growth.png
│       ├── rfm_segment_distribution.png
│       ├── rfm_share_comparison.png
│       └── rfm_recency_vs_frequency.png
│
├── dashboard/
│   ├── index.html                    # Sleek interactive BI dashboard
│   ├── data.js                       # Pre-aggregated dashboard data payload
│   └── dashboard_mockup.md           # Dashboard proposed KPIs & layout wireframe
│
└── README.md                         # Project documentation (This file)
```

---

## 🛠️ Execution & Deployment

### 1. Installation
Ensure Python 3.x is installed with the analytical dependencies:
```bash
pip install pandas numpy matplotlib seaborn tabulate
```

### 2. Generate Analysis and Visualizations
Execute the Python scripts in order to rebuild database and reports:
```bash
# Run cohort retention matrices & LTV growth curves
python src/cohort_analysis.py

# Run RFM scores ranking & segment clustering
python src/rfm_analysis.py

# Export aggregated metrics for BI dashboard
python src/generate_dashboard_data.py
```

### 3. Deploy the Interactive BI Dashboard (GitHub Pages)
An interactive dark-mode dashboard is fully implemented in `dashboard/index.html`. 
To host this dashboard live:
1. Go to your **GitHub Repository Settings** -> **Pages** section.
2. Under **Build and deployment** -> **Source**, select **Deploy from a branch**.
3. Under **Branch**, select **`main`** (or `master`) and the folder **`root`** (or select the `/dashboard` folder if you move it, but keeping it in the root is easiest), then click **Save**.
4. Within minutes, your interactive dashboard will be live at:  
   `https://harshsinghps57-spec.github.io/Deep-Dive-Analysis-Interactive-Dashboard/dashboard/index.html`

---

## 🔑 Critical Deep-Dive Findings

### 1. Cohort Retention Decay
- Across all quarters, there is a major post-acquisition drop-off in `Q1` where customer retention drops to **12–22%**.
- However, retention rates flatline and stabilize around **15–26%** from `Q2` through `Q12`, showing solid long-term brand loyalty for repeat buyers.
- Retained customers generate compounding value: a customer acquired for **$300** initially contributes over **$1,500** in cumulative LTV by `Q12`.

### 2. RFM Customer Segments
- **Champions & Loyalists** (33.29% of customers) generate **49.19% of total revenue** ($1.13 Million). *Strategy: Reward loyalty, protect high margins (no discounting).*
- **At Risk** (25.22% of customers) is the single largest segment by revenue share (**30.15% | $692,546**), but has not made a purchase in over 8 months. *Strategy: Urgently trigger reactivate win-back campaigns offering targeted 15% discounts.*
- **Potential Loyalists** (18.41% of customers) are new buyers. *Strategy: Deliver onboarding recommendations to build recurring habits.*

---

## 👤 Author

**Harsh Singh**  
Intern @ ApexPlanet Software Pvt. Ltd.  
[GitHub Profile](https://github.com/harshsinghps57-spec)
