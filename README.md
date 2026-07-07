# ECB Customer Engagement & Retention Analytics

## 🎯 Project Overview

A multi-dimensional behavioral analytics framework for banking customer retention strategy in the European banking sector. Dataset: **10,000 retail bank customers** across France, Germany, and Spain (2025).

This repository contains:

1. **`app.py`** — Streamlit analytics dashboard (7 tabs, 5 strategic KPIs)
2. **`transform_data.py`** — Reproducible feature engineering pipeline (raw → 59-feature dataset)
3. **`compute_stats.py`** — Ground-truth statistics extractor (verified against raw data)
4. **`data/`** — Raw (14 cols) and transformed (56 analytical cols, PII-free) datasets

> **Note:** The research manuscript (`ECB_Research_Manuscript.docx`) and its generator (`generate_manuscript.py`) are **not included in this repository** — they are available locally. Run `python generate_manuscript.py` locally to produce the 15–20 page Word document.

> **✅ 107/107 CROSS-FILE CHECKS PASSED | 155/155 DATASET INTEGRITY CHECKS PASSED**

---

## 📁 Project Structure

```
📦 ECB_Retention_strategy/  (GitHub repository)
├── 📄 app.py                            # Streamlit dashboard (run this)
├── 📄 transform_data.py                 # Feature engineering pipeline
├── 📄 compute_stats.py                  # Ground-truth stats extractor
├── 📄 README.md                         # This file
├── 📄 requirements.txt                  # Python dependencies
├── 📄 .gitignore                        # Excludes manuscript & generator
└── 📊 data/
    ├── European_Bank.csv                # Raw dataset (10,000 rows, 14 vars)
    └── European_Bank_Transformed.csv    # Analytical dataset (56 cols, PII-free)
```

> ℹ️ `ECB_Research_Manuscript.docx` and `generate_manuscript.py` are **local only** (gitignored). They are never pushed to GitHub.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch Streamlit Dashboard

```bash
streamlit run app.py
```


### 3. Verify Stats Against Raw Data

```bash
python compute_stats.py
```

---

## 📊 Key Findings — VERIFIED VALUES (from `compute_stats.py`)

### Portfolio Overview

| Metric | Value | Source |
|--------|-------|--------|
| Total Customers | **10,000** | Raw data |
| Churned Customers | **2,037** | Raw data |
| Overall Churn Rate | **20.37%** | Raw data ✅ |
| Retained Customers | **7,963** | Raw data |

### Engagement Metrics

| Metric | Value | Verified |
|--------|-------|---------|
| Active Members | 5,151 (51.51%) | ✅ |
| Active Churn Rate | **14.27%** | ✅ |
| Inactive Members | 4,849 (48.49%) | ✅ |
| Inactive Churn Rate | **26.85%** | ✅ |
| **Engagement Retention Ratio (ERR)** | **1.882×** | ✅ |

### Product Utilization (Non-Linear Paradox)

| Products | Customers | Churn Rate | Status |
|----------|-----------|------------|--------|
| 1 (Single) | 5,084 | **27.71%** | High risk |
| 2 (Dual) | 4,590 | **7.58%** | ✅ OPTIMAL |
| 3 (Multi) | 266 | **82.71%** | ⚠️ CRITICAL |
| 4 (Full) | 60 | **100.00%** | 🚨 CATASTROPHIC |

> Active+Multi-Product churn: **9.66%** | Inactive+Single-Product churn: **36.65%**

### Geographic Distribution

| Country | Customers | Churned | Churn Rate |
|---------|-----------|---------|------------|
| France | 5,014 (50.14%) | 810 | **16.15%** |
| Germany | 2,509 (25.09%) | 814 | **32.44%** |
| Spain | 2,477 (24.77%) | 413 | **16.67%** |

### Gender

| Gender | Customers | Churned | Churn Rate |
|--------|-----------|---------|------------|
| Female | 4,543 | 1,139 | **25.07%** |
| Male | 5,457 | 898 | **16.46%** |

### Relationship Strength Index (RSI) Bands

| RSI Band | Count | Churn Rate | Avg RSI |
|----------|-------|------------|---------|
| Very Weak (0-2) | 223 | **48.88%** | 1.68 |
| Weak (2-4) | 2,209 | **36.62%** | 3.20 |
| Moderate (4-6) | 3,327 | **19.12%** | 5.10 |
| Strong (6-8) | 3,051 | **13.27%** | 7.00 |
| Very Strong (8-10) | 1,190 | **6.55%** | 8.70 |

> RSI correlation with churn: **r = −0.271** (strongest single predictor)

### Engagement Tiers

| Tier | Count | Churned | Churn Rate | Avg Balance | Avg RSI |
|------|-------|---------|------------|-------------|---------|
| Active-Engaged | 2,588 | 250 | **9.66%** | €53,071 | 7.88 |
| Active-Low-Product | 2,563 | 485 | **18.92%** | €98,902 | 6.27 |
| Inactive-Disengaged | 3,602 | 922 | **25.60%** | €52,304 | 4.02 |
| Inactive-High-Balance | 1,247 | 380 | **30.47%** | €148,858 | 4.16 |

### Strategic KPI Flags

| KPI | Count | Churn Rate | Priority |
|-----|-------|------------|---------|
| High-Balance Disengaged | **1,247** (12.47%) | **30.47%** | 🚨 Critical |
| Sticky Customer | **1,015** (10.15%) | **9.26%** | ✅ Replicate |
| Silent Churn Risk | **828** | **33.45%** | ⚠️ High |
| Salary-Balance Mismatch | **891** | **14.81%** | Cross-sell |
| Wealth Engagement Gap | **1,231** | — | Activate |

### Balance Analysis

| Metric | Value |
|--------|-------|
| Mean Balance | **€76,485.89** |
| Std Balance | **€62,397.41** |
| Zero Balance Customers | **3,617 (36.17%)** |
| Zero Balance Churn Rate | **13.82%** |
| Non-Zero Balance Churn Rate | **24.08%** |

### Demographic Highlights

| Metric | Value |
|--------|-------|
| Mean Age (overall) | **38.92 years** |
| Mean Age (churned) | **44.84 years** |
| Mean Age (retained) | **37.41 years** |
| Age gap (churned - retained) | **7.43 years** |
| Mean Credit Score | **650.53** |
| Mean Tenure | **5.01 years** |
| Mean Estimated Salary | **€100,090.24** |

### Retention Risk Score Bands

| Risk Band | Count | Realised Churn |
|-----------|-------|----------------|
| Very Low Risk (<25) | 2,613 | **5.89%** |
| Low Risk (25-45) | 2,937 | **17.02%** |
| Moderate Risk (45-60) | 1,746 | **13.34%** |
| High Risk (60-75) | 1,936 | **35.85%** |
| Very High Risk (>75) | 768 | **59.38%** |

> RetentionRiskScore correlation with churn: **r = +0.349** (strongest positive predictor)

### Key Correlations with Churn (Pearson r)

| Feature | r | Direction |
|---------|---|-----------|
| RelationshipStrengthIndex | **−0.271** | Protective |
| IsActiveMember | −0.156 | Protective |
| NumOfProducts | −0.048 | Protective |
| CreditScore | −0.027 | Protective |
| Tenure | −0.014 | Protective |
| HasCrCard | −0.007 | Protective |
| EstimatedSalary | +0.012 | Risk |
| Balance | +0.119 | Risk |
| Age | +0.285 | Risk |
| RetentionRiskScore | **+0.349** | Risk |

---

## 📈 RSI Formula

**RSI [0–10] = Activity + ProductDepth + CreditCard + Tenure + Balance**

| Component | Range | Logic |
|-----------|-------|-------|
| Activity | 0–3 pts | IsActiveMember × 3 |
| Product Depth | 0–3 pts | 1 prod=1.0, 2 prod=3.0, 3 prod=0.5, 4 prod=0.0 |
| Credit Card | 0–1 pt | HasCrCard × 1 |
| Tenure | 0–2 pts | min(Tenure/5, 2.0) |
| Balance Tier | 0–1 pt | min(BalanceTierRank/4, 1.0) |

---

## 🔐 Ethical & Privacy Compliance

- ✅ All data anonymized (no PII)
- ✅ GDPR compliant aggregate analysis
- ✅ No personally identifiable information in dataset
- ✅ Transparent, reproducible methodology

---

## 🛠️ Technical Stack

| Package | Use |
|---------|-----|
| `pandas >= 1.5.0` | Data manipulation |
| `numpy >= 1.23.0` | Numerical computation |
| `streamlit >= 1.20.0` | Dashboard framework |
| `plotly >= 5.10.0` | Visualizations |
| `python-docx >= 0.8.11` | Word document generation |

---

## 🔗 Repository

GitHub: https://github.com/ganapathi-ai/ECB_Retention_strategy

**Author:** Ganapathi kakarla

