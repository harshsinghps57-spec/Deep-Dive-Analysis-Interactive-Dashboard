# Customer Deep-Dive & Segmentation Dashboard Mock-up Proposal

This document outlines the business specifications, structural design, and wireframes for the **Week 3 Customer Deep-Dive & Interactive Dashboard** built on the Superstore dataset. 

An interactive, dynamic mock-up implementation is available at [dashboard/index.html](file:///C:/Users/user/.gemini/antigravity/scratch/Deep-Dive-Analysis-Interactive-Dashboard/dashboard/index.html).

---

## 📈 Formally Defined Core Customer KPIs

To measure customer growth, loyalty, and lifecycle health, the dashboard surfaces four core metrics:

| KPI Name | Formula | Business Rationale & Relevance |
| :--- | :--- | :--- |
| **Total Sales (Revenue)** | `SUM(Sales)` | Baseline financial size of the customer base. |
| **Total Customers** | `COUNT(Distinct Customer ID)` | Size of the active customer directory. |
| **Returning Customer Rate** | `(COUNT(Customers with >= 2 Orders) / Total Customers) * 100` | Measures loyalty. Higher returning rates reduce high customer acquisition costs. |
| **Average Order Value (AOV)** | `Total Sales / Total Orders` | Average transaction size. Key driver for top-line revenue growth. |

---

## 🖼️ Dashboard Tabbed Wireframe Design

The user interface uses a **Tabbed Layout** to separate the two major analysis modules:

### Module 1: Cohort Retention & Lifetime Value (LTV)
```
+------------------------------------------------------------------------------------+
|  [Logo] DEEP-DIVE CUSTOMER DASHBOARD                              [Segment] [Region] |
+------------------------------------------------------------------------------------+
|  [Tab 1: Cohort Retention & LTV (ACTIVE)]     [Tab 2: RFM Customer Segmentation]   |
+------------------------------------------------------------------------------------+
|  +---------------------+ +---------------------+ +---------------------+ +-------+  |
|  | TOTAL REVENUE       | | TOTAL CUSTOMERS     | | RETURNING RATE      | | AOV   |  |
|  | $2,297,201          | | 793                 | | 90.7%               | | $230  |  |
|  +---------------------+ +---------------------+ +---------------------+ +-------+  |
+------------------------------------------------------------------------------------+
|  CHART 1: Dynamic Cohort Retention Matrix Heatmap (HTML Dynamic Grid)               |
|  Grouped by First Purchase Quarter (e.g. 2014-Q1). Displays % of customers returning|
|  in Index Quarters Q0, Q1, Q2, ..., Q12. Cell opacity scales with retention value.  |
|  +-------------------------+------+------+------+------+------+------+----------+  |
|  | Cohort   | Size | Q0    | Q1   | Q2   | Q3   | Q4   | ...  | Q12  |          |  |
|  | 2014-Q1  | 285  | 100%  | 15%  | 18%  | 22%  | 20%  | ...  | 25%  | (Heatmap) |  |
|  +-------------------------+------+------+------+------+------+------+----------+  |
+------------------------------------------------------------------------------------+
|  CHART 2: Cohort Customer Lifetime Value (LTV) Growth Curves                       |
|  Line chart displaying cumulative cohort spend over subsequent quarters.            |
|  (Renders lines for 2014 cohorts showing cumulative slope values up to $1,000+).     |
+------------------------------------------------------------------------------------+
```

### Module 2: RFM Customer Segmentation Explorer
```
+------------------------------------------------------------------------------------+
|  [Tab 1: Cohort Retention & LTV]     [Tab 2: RFM Customer Segmentation (ACTIVE)]   |
+------------------------------------------------------------------------------------+
|  +--------------------------------------------+ +----------------------------------+  |
|  | CHART 3: Customer RFM Segment Sizes        | | CHART 4: Segment Revenue Share   |  |
|  | (Bar Chart - Champions, Loyal, At Risk)     | | (Doughnut Chart of Monetary $)   |  |
|  +--------------------------------------------+ +----------------------------------+  |
+------------------------------------------------------------------------------------+
|  INTERACTIVE EXPLORER SECTION:                                                     |
|  Select a Segment Option:     | Segment Details Pane:                              |
|  [ ] Champions (106)          | Metrics: Counts, Recency, Frequency, Total Sales.  |
|  [ ] Loyalists (158)          | Strategy Alert: recommended marketing plan.        |
|  [x] At Risk (200)            | Top 5 Highest Spenders Customer Table:             |
|  [ ] Potential Loyalist (146) | ID     | Name        | Recency | Orders | Total $   |
|  [ ] Hibernating (183)        | SM-20  | Sean Miller | 12d     | 5      | $25,043   |
+------------------------------------------------------------------------------------+
```
