# Customer Growth, Cohort Retention & RFM Segmentation Deep-Dive Report

This report presents a comprehensive customer analytics deep-dive using the Superstore transaction dataset. The analysis was executed in Python to model cohort lifecycle retention rates, Lifetime Value (LTV) curves, and Customer RFM Segmentation.

---

## 1. Executive Summary
To optimize customer acquisition cost (CAC) and improve retention, we analyzed **793 unique customers** across **9,994 transactions** spanning 2014–2017. 
Our primary objective was to uncover cohort-level engagement patterns and establish an actionable RFM (Recency, Frequency, Monetary) segmentation model to drive targeted marketing campaigns.

**Key Deliverable**: An interactive BI dashboard mock-up visualizing these findings is available at [dashboard/index.html](file:///C:/Users/user/.gemini/antigravity/scratch/Deep-Dive-Analysis-Interactive-Dashboard/dashboard/index.html).

---

## 2. Cohort Retention & Lifetime Value (LTV) Deep-Dive

Customers were grouped into quarterly cohorts based on the quarter of their very first transaction (e.g., `2014-Q1`). We tracked their purchasing activity over subsequent index quarters (`Q0` to `Q12`).

### 📌 Cohort Retention Key Findings
- **The Initial Churn Gap**: The transition from `Q0` (first purchase) to `Q1` (second quarter) exhibits a steep drop-off across all cohorts, with retention rates falling between **12% and 22%**. This indicates a critical post-onboarding engagement drop.
- **Long-Term Stabilization**: After `Q2`, the customer decay rate flatlines. Retention stabilizes in the **15% to 26%** range, showing that once a customer places their 3rd order, they remain highly active long-term.
- **Seasonal Cohorts**: Cohorts acquired in **Q4** (holiday seasons) generally demonstrate 2–3% higher initial retention rates compared to Q1 cohorts, showing higher initial purchase intent.

### 📌 Customer Lifetime Value (LTV) Curves
- Across all cohorts, LTV curves demonstrate a consistent, near-linear upward trajectory.
- For the early 2014 cohorts, the average cumulative spend per customer starts at **$250–$350 in Q0** and surpasses **$1,000+ by Q8** (2 years) and **$1,500+ by Q12** (3 years).
- This consistent LTV growth highlights that the long-term value of retained customers is massive, justifying a higher customer acquisition cost (CAC) for initial acquisition.

---

## 3. RFM Customer Segmentation Deep-Dive

Recency, Frequency, and Monetary scores were calculated for each customer. Customers were grouped into 5 core segments:

| RFM Segment | Customer Count | Customer Share % | Total Sales ($) | Revenue Share % | Average Recency | Avg. Purchase Frequency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Champions** | 106 | 13.37% | $560,498.82 | 24.40% | 25.5 Days | 9.3 Orders |
| **Loyalists** | 158 | 19.92% | $569,388.86 | 24.79% | 50.7 Days | 7.7 Orders |
| **Potential Loyalists** | 146 | 18.41% | $301,602.11 | 13.13% | 45.2 Days | 4.1 Orders |
| **At Risk** | 200 | 25.22% | $692,546.95 | 30.15% | 257.1 Days | 6.7 Orders |
| **Hibernating** | 183 | 23.08% | $173,164.13 | 7.54% | 264.8 Days | 4.8 Orders |
| **TOTAL** | **793** | **100%** | **$2,297,201** | **100%** | **150.3 Days** | **6.3 Orders** |

### 📌 Segment Analysis & Marketing Action Plan

#### 1. Champions (13.37% Customers | 24.40% Revenue)
- *Profile:* Purchased recently, order frequently, and spend heavily.
- *Strategy:* Avoid discounting (they will buy anyway). Focus on VIP recognition, early-access programs, referral incentives, and personalized high-value reviews.

#### 2. Loyalists (19.92% Customers | 24.79% Revenue)
- *Profile:* Very consistent buying history and solid spend.
- *Strategy:* Leverage cross-selling and upselling (e.g. recommend high-margin accessories in Technology). Introduce a point-based loyalty program to keep them engaged.

#### 3. Potential Loyalists (18.41% Customers | 13.13% Revenue)
- *Profile:* Recent buyers, but low order frequency so far.
- *Strategy:* Standard nurturing. Deliver onboarding welcome emails, suggest top-selling office products, and offer a moderate 10% discount on their second/third orders to establish purchasing habits.

#### 4. At Risk (25.22% Customers | 30.15% Revenue)
- *⚠️ Critical Threat/Opportunity:* This is your largest segment by revenue share (30.15%) but has not made a purchase in **over 8 months** (average recency of 257 days).
- *Strategy:* Launch an aggressive customer reactivation campaign. Send personalized email win-back offers with high-value promotions (e.g., 15–20% discounts or free delivery) to recapture their spend before they churn permanently.

#### 5. Hibernating (23.08% Customers | 7.54% Revenue)
- *Profile:* Inactive, infrequent buyers with low historical value.
- *Strategy:* Minimize marketing costs. Run low-cost automated email campaigns for end-of-season clearance sales. Do not spend paid acquisition dollars retargeting this group.
