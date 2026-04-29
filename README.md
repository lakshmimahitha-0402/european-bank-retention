# 🏦 European Bank — Customer Retention Intelligence

> A data-driven analytics project designed to identify customer churn patterns and deliver actionable retention strategies using an interactive Streamlit dashboard.

---

## 📌 Project Overview

Customer retention is a critical challenge in the banking sector. This project analyses 10,000 customer records to uncover key drivers of churn based on customer engagement, product utilization, demographics, financial behaviour, and relationship strength.

The project delivers:

- 📊 Interactive Streamlit Dashboard
- 📄 Executive Summary
- 📘 Research Paper
- 💡 Business Insights & Recommendations

---

## 🎯 Objectives

- Identify high-risk customer segments
- Analyse the impact of engagement and product depth on churn
- Detect high-value customers silently at risk
- Build a retention-focused analytical framework
- Provide actionable, business-ready recommendations

---

## 📊 Key Insights

- 📉 **20.37% overall churn rate** — 1 in 5 customers leaves
- 🌍 **Germany has the highest churn at 32.4%** — nearly double France and Spain
- 📦 **2 products = lowest churn (7.6%)** — the optimal product mix
- ⚠️ **3–4 products = 83–100% churn** — over-bundling risk
- 👤 **Inactive customers churn 12.6 points more** than active members
- 💰 **1,247 high-value inactive customers** identified as at-risk premium segment
- 👵 **Age 51–60 group shows highest churn at 56.2%**

---

## 🧠 Feature Engineering

### 🔹 Engagement Profiles

Customers segmented into four behavioural groups based on activity and product count:

- Active Engaged
- Active Low-Product
- Inactive Disengaged
- Inactive High-Balance

### 🔹 Relationship Strength Index (RSI)

A composite score (0–1) measuring customer relationship depth:

```
RSI = 0.4 × Activity
    + 0.3 × Product Depth
    + 0.2 × Tenure
    + 0.1 × Credit Card Ownership
```

### 🔹 At-Risk Premium Flag

Customers flagged when:

- Balance > €127,644 (top 25%) **AND**
- IsActiveMember = 0

These 1,247 customers represent the highest financial risk segment.

---

## 🖥️ Dashboard Features

### 📌 4 Interactive Pages

**Engagement Overview**

- Churn distribution pie chart
- Geography churn bar chart
- Engagement profile and age group analysis

**Product Utilization**

- Product count vs churn rate
- Customer distribution by product
- Geography × Products heatmap

**High-Value Risk Analysis**

- Balance distribution by churn status
- Balance tier churn breakdown
- At-risk premium customer table + CSV download

**Retention Strength**

- RSI scoring by tier
- Tenure trend analysis
- Credit card stickiness and credit score bands

### 🎛️ Real-Time Sidebar Filters

- Geography (Country)
- Gender
- Number of Products
- Member Status (Active / Inactive)
- Minimum Balance
- Minimum Credit Score

---

## 💡 Business Recommendations

- 🎯 Re-engage 1,247 high-value inactive customers with personalised outreach
- 📦 Optimise product bundling strategy — focus on the 2-product sweet spot
- 🌍 Launch a Germany-specific retention programme (32.4% churn)
- 👵 Design a senior-friendly banking experience for the 51–60 age group
- 👩 Introduce targeted loyalty programmes for female customers

---

## 🛠️ Tech Stack

- **Python** — Data processing and analytics
- **Streamlit** — Interactive dashboard
- **Pandas / NumPy** — Data manipulation
- **Matplotlib / Seaborn** — Visualisation

---

## 📁 Repository Structure

```
european-bank-retention-analysis/
│
├── bank_app.py
├── European_Bank.csv
├── unified logo.png
├── requirements.txt
├── README.md
│
├── notebooks/
│   └── European_Bank_Analysis.ipynb
│
└── reports/
    ├── European_Bank_Research_Paper.docx
    └── European_Bank_Executive_Summary.docx
```

---

## ⚙️ How to Run the App

```bash
pip install -r requirements.txt
streamlit run bank_app.py
```

---

## 🧠 Business Value

This project shifts customer retention strategy from reactive churn tracking to proactive engagement management, enabling the bank to:

- Identify and re-engage high-value inactive customers before they silently exit
- Optimise product offerings to avoid the over-bundling trap
- Address region-specific churn drivers with targeted country programmes
- Use RSI scoring as an early warning system for disengaging customers
- Support data-driven retention campaigns grounded in behavioural insights

---

## ⚠️ Limitations

- No time-series data — behavioural trends over time cannot be tracked
- Binary activity flag — degree of engagement depth is not captured
- Estimated salary may not reflect actual verified income
- Churn defined only as account exit, not partial disengagement

---

## 📌 Author

Data Analyst Internship Project – Customer Retention & Behavioural Analytics

**Lakshmi Mahitha Noudu** | Unified Mentor | Mentored by Sai Prasad Kagne | April 2026
