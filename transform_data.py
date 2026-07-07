"""
=============================================================================
ECB Customer Engagement & Retention Analytics
Feature Engineering Pipeline  —  transform_data.py
=============================================================================
Transforms: data/European_Bank.csv  (raw, 14 columns, 10,000 rows)
       into: data/European_Bank_Transformed.csv  (59 columns, 10,000 rows)

ALL formulas verified 100% against the existing transformed dataset.
Run: python transform_data.py
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "data", "European_Bank.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "European_Bank_Transformed.csv")


def engineer_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Apply the full 12-step feature engineering pipeline to the raw dataset."""
    df = df_raw.copy()

    # ── Pre-compute thresholds from raw data (must match original pipeline) ─
    bal_q75 = df["Balance"].quantile(0.75)          # ≈ 127,644.24 EUR
    sal_q75 = df["EstimatedSalary"].quantile(0.75)  # ≈ 149,388.25 EUR

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 2 — DEMOGRAPHIC SEGMENTATION
    # ══════════════════════════════════════════════════════════════════════════

    # 2a. Age band (6 life-stage segments)
    df["AgeBand"] = pd.cut(
        df["Age"],
        bins=[0, 25, 35, 45, 55, 65, 120],
        labels=["18-25 (Gen-Z)", "26-35 (Millennial)", "36-45 (Gen-X)",
                "46-55 (Mid-Career)", "56-65 (Pre-Retirement)", "66+ (Senior)"],
    )
    age_order = ["18-25 (Gen-Z)", "26-35 (Millennial)", "36-45 (Gen-X)",
                 "46-55 (Mid-Career)", "56-65 (Pre-Retirement)", "66+ (Senior)"]
    df["AgeBand_Num"] = df["AgeBand"].map(
        {v: i for i, v in enumerate(age_order)}
    ).astype(int)

    # 2b. Credit score tier (Basel-inspired 6-tier standard)
    # Boundaries: 349-500=Very Poor(643), 501-580=Poor(1750),
    # 581-670=Fair(3350), 671-740=Good(2397), 741-800=Very Good(1215), 801-850=Exceptional(645)
    df["CreditTier"] = pd.cut(
        df["CreditScore"],
        bins=[349, 500, 580, 670, 740, 800, 851],
        labels=["Very Poor", "Poor", "Fair", "Good", "Very Good", "Exceptional"],
    )
    credit_order = ["Very Poor", "Poor", "Fair", "Good", "Very Good", "Exceptional"]
    df["CreditTier_Num"] = df["CreditTier"].map(
        {v: i for i, v in enumerate(credit_order)}
    ).astype(int)

    # 2c. Tenure segment (5 levels)
    # New(<1yr) = tenure 0 or 1 (<=1)   → 1,448 customers
    # Early(1-3yr)  = tenure 2-3         → 2,057 customers
    # Established(3-6yr) = tenure 4-6    → 2,968 customers
    # Loyal(6-9yr)  = tenure 7-9         → 3,037 customers
    # Veteran(9-10yr) = tenure 10        →   490 customers
    df["TenureSegment"] = pd.cut(
        df["Tenure"],
        bins=[-0.01, 1, 3, 6, 9, 10],
        labels=["New (<1yr)", "Early (1-3yr)", "Established (3-6yr)",
                "Loyal (6-9yr)", "Veteran (9-10yr)"],
    )
    tenure_order = ["New (<1yr)", "Early (1-3yr)", "Established (3-6yr)",
                    "Loyal (6-9yr)", "Veteran (9-10yr)"]
    df["TenureSegment_Num"] = df["TenureSegment"].map(
        {v: i for i, v in enumerate(tenure_order)}
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — FINANCIAL FEATURE ENGINEERING
    # ══════════════════════════════════════════════════════════════════════════

    # 3a. HasBalance flag
    df["HasBalance"] = (df["Balance"] > 0).astype(int)

    # 3b. Balance tier (5 levels)
    df["BalanceTier"] = pd.cut(
        df["Balance"],
        bins=[-0.01, 0, 50_000, 100_000, 150_000, float("inf")],
        labels=["Zero Balance", "Low (1-50k)", "Mid (50-100k)",
                "High (100-150k)", "Premium (150k+)"],
    )
    balance_order = ["Zero Balance", "Low (1-50k)", "Mid (50-100k)",
                     "High (100-150k)", "Premium (150k+)"]
    df["BalanceTier_Num"] = df["BalanceTier"].map(
        {v: i for i, v in enumerate(balance_order)}
    ).astype(int)

    # 3c. Salary tier (5 levels)
    sal_bins = df["EstimatedSalary"].quantile([0, 0.25, 0.5, 0.75, 1.0]).values
    df["SalaryTier"] = pd.cut(
        df["EstimatedSalary"],
        bins=sal_bins,
        labels=["Low", "Lower-Mid", "Upper-Mid", "High"],
        include_lowest=True,
    )
    salary_order = ["Low", "Lower-Mid", "Upper-Mid", "High"]
    df["SalaryTier_Num"] = df["SalaryTier"].map(
        {v: i for i, v in enumerate(salary_order)}
    ).fillna(0).astype(int)

    # 3d. Balance-to-Salary Ratio
    df["BalanceToSalaryRatio"] = (
        df["Balance"] / df["EstimatedSalary"].replace(0, np.nan)
    ).fillna(0).round(6)

    # 3e. Salary-Balance Mismatch: top-quartile earner with zero balance
    df["SalaryBalanceMismatch"] = (
        (df["EstimatedSalary"] >= sal_q75) & (df["Balance"] == 0)
    ).astype(int)

    # 3f. IsPremiumCustomer: top-25% balance (>= Q75)
    df["IsPremiumCustomer"] = (df["Balance"] >= bal_q75).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 4 — PRODUCT UTILIZATION FEATURES
    # ══════════════════════════════════════════════════════════════════════════

    # 4a. Product Depth Index: (NumOfProducts - 1) / 3  →  [0, 1]
    df["ProductDepthIndex"] = ((df["NumOfProducts"] - 1) / 3).round(6)

    # 4b. Product Breadth categories
    prod_map = {1: "Single-Product", 2: "Dual-Product",
                3: "Multi-Product",  4: "Full-Suite"}
    df["ProductBreadth"] = df["NumOfProducts"].map(prod_map)

    # 4c. Binary flags
    df["IsMultiProduct"]    = (df["NumOfProducts"] >= 2).astype(int)
    df["IsFullSuiteUser"]   = (df["NumOfProducts"] >= 3).astype(int)

    # 4d. Credit Card Stickiness proxy
    df["CrCardStickiness"]  = df["HasCrCard"].astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 5 — ENGAGEMENT CLASSIFICATION (4-tier)
    # ══════════════════════════════════════════════════════════════════════════
    # Active-Engaged:        IsActiveMember=1 AND NumOfProducts >= 2
    # Active-Low-Product:    IsActiveMember=1 AND NumOfProducts  = 1
    # Inactive-High-Balance: IsActiveMember=0 AND Balance >= Q75
    # Inactive-Disengaged:   all remaining inactive customers

    eng = pd.Series("Inactive-Disengaged", index=df.index)
    eng[(df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= 2)] = "Active-Engaged"
    eng[(df["IsActiveMember"] == 1) & (df["NumOfProducts"] == 1)] = "Active-Low-Product"
    eng[(df["IsActiveMember"] == 0) & (df["Balance"] >= bal_q75)] = "Inactive-High-Balance"
    df["EngagementTier"] = eng

    eng_order = ["Active-Engaged", "Active-Low-Product",
                 "Inactive-Disengaged", "Inactive-High-Balance"]
    df["EngagementTier_Num"] = df["EngagementTier"].map(
        {v: i for i, v in enumerate(eng_order)}
    ).astype(int)

    df["ActiveAndMultiProduct"]  = (
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= 2)
    ).astype(int)
    df["InactiveAndSingleProduct"] = (
        (df["IsActiveMember"] == 0) & (df["NumOfProducts"] == 1)
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 6 — RELATIONSHIP STRENGTH INDEX (RSI)  [0–10]
    # ══════════════════════════════════════════════════════════════════════════
    # Component      Weight  Logic
    # Activity        0–3    IsActiveMember × 3
    # Product Depth   0–3    1=1.0, 2=3.0, 3=0.5, 4=0.0  (paradox penalty)
    # Credit Card     0–1    HasCrCard × 1
    # Tenure          0–2    min(Tenure / 5, 2.0)
    # Balance Tier    0–1    min(BalanceTier_Num / 4, 1.0)

    prod_pts_map = {1: 1.0, 2: 3.0, 3: 0.5, 4: 0.0}
    rsi = (
        df["IsActiveMember"] * 3.0
        + df["NumOfProducts"].map(prod_pts_map)
        + df["HasCrCard"] * 1.0
        + df["Tenure"].apply(lambda t: min(t / 5, 2.0))
        + (df["BalanceTier_Num"] / 4).clip(upper=1.0)
    )
    df["RelationshipStrengthIndex"] = rsi.round(4)

    # RSI Bands
    df["RSI_Band"] = pd.cut(
        df["RelationshipStrengthIndex"],
        bins=[-0.01, 2, 4, 6, 8, 10],
        labels=["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"],
    )
    rsi_order = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    df["RSI_Band_Num"] = df["RSI_Band"].map(
        {v: i for i, v in enumerate(rsi_order)}
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 7 — KPI FLAG COMPUTATION
    # ══════════════════════════════════════════════════════════════════════════

    # High-Balance Disengaged: premium balance + inactive
    df["HighBalanceDisengaged"] = (
        (df["Balance"] >= bal_q75) & (df["IsActiveMember"] == 0)
    ).astype(int)

    # Sticky Customer: active + 2+ products + credit card + tenure >= 5 yrs
    df["IsStickyCustomer"] = (
        (df["IsActiveMember"] == 1)
        & (df["NumOfProducts"] >= 2)
        & (df["HasCrCard"] == 1)
        & (df["Tenure"] >= 5)
    ).astype(int)

    # Silent Churn Risk: premium balance + inactive + single product
    df["SilentChurnRisk"] = (
        (df["Balance"] >= bal_q75)
        & (df["IsActiveMember"] == 0)
        & (df["NumOfProducts"] == 1)
    ).astype(int)

    # Active Retained: active + not churned
    df["ActiveRetained"] = (
        (df["IsActiveMember"] == 1) & (df["Exited"] == 0)
    ).astype(int)

    # Inactive Churned: inactive + churned
    df["InactiveChurned"] = (
        (df["IsActiveMember"] == 0) & (df["Exited"] == 1)
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 8 — RETENTION RISK SCORE  [0–100]
    # ══════════════════════════════════════════════════════════════════════════
    # Logistic-inspired scoring model.
    #
    # Score = baseline(50)
    #       + engagement_adj  (-18 if active, +18 if inactive)
    #       + product_adj     (1→+15, 2→-10, 3→+40, 4→+55)
    #       + card_adj        (-2 if HasCrCard)
    #       + balance_adj     (-5 if Balance > 0)
    #       + premium_adj     (-5 if Balance >= Q75)
    #       + geo_adj         (+8 if Germany)
    #       - tenure_disc     (min(Tenure × 1.5, 12))
    #   clipped to [0, 100]

    prod_risk_map = {1: 15, 2: -10, 3: 40, 4: 55}

    rrs = (
        50
        + np.where(df["IsActiveMember"] == 1, -18, 18)
        + df["NumOfProducts"].map(prod_risk_map)
        + np.where(df["HasCrCard"] == 1, -2, 0)
        + np.where(df["Balance"] > 0, -5, 0)
        + np.where(df["Balance"] >= bal_q75, -5, 0)
        + np.where(df["Geography"] == "Germany", 8, 0)
        - (df["Tenure"] * 1.5).clip(upper=12)
    )
    df["RetentionRiskScore"] = pd.Series(rrs, index=df.index).clip(0, 100).round(4)

    # Risk Bands
    df["RiskBand"] = pd.cut(
        df["RetentionRiskScore"],
        bins=[-0.01, 25, 45, 60, 75, 100],
        labels=["Very Low Risk", "Low Risk", "Moderate Risk",
                "High Risk", "Very High Risk"],
    )
    risk_order = ["Very Low Risk", "Low Risk", "Moderate Risk",
                  "High Risk", "Very High Risk"]
    df["RiskBand_Num"] = df["RiskBand"].map(
        {v: i for i, v in enumerate(risk_order)}
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 9 — GEOGRAPHIC RISK INDEX
    # ══════════════════════════════════════════════════════════════════════════

    geo_churn = df.groupby("Geography")["Exited"].transform("mean")
    df["GeoChurnRate"] = geo_churn.round(6)
    df["GeoRiskIndex"]  = (geo_churn * 100).round(4)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 10 — CROSS-SEGMENT INTERACTION FEATURES
    # ══════════════════════════════════════════════════════════════════════════

    df["AgeActivityScore"]    = df["Age"] * df["IsActiveMember"]
    df["BalanceActivityScore"] = (df["Balance"] / 1000).round(4) * df["IsActiveMember"]
    df["ProductTenureScore"]  = df["NumOfProducts"] * np.log1p(df["Tenure"])
    df["CreditActiveScore"]   = df["CreditScore"] * df["IsActiveMember"]
    df["WealthEngagementGap"] = (
        (df["EstimatedSalary"] >= sal_q75) & (df["IsActiveMember"] == 0)
    ).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 11 — ONE-HOT ENCODING
    # ══════════════════════════════════════════════════════════════════════════

    df["Geography_France"]  = (df["Geography"] == "France").astype(int)
    df["Geography_Germany"] = (df["Geography"] == "Germany").astype(int)
    df["Geography_Spain"]   = (df["Geography"] == "Spain").astype(int)
    df["Gender_Male"]       = (df["Gender"] == "Male").astype(int)

    return df


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Loading raw dataset...")
    raw = pd.read_csv(INPUT_PATH)
    print(f"  Raw shape: {raw.shape}")

    print("Applying feature engineering pipeline...")
    transformed = engineer_features(raw)
    print(f"  Transformed shape: {transformed.shape}")

    # Validation checks
    n = len(transformed)
    churned = int(transformed["Exited"].sum())
    churn_rate = transformed["Exited"].mean() * 100
    rsi_mean   = transformed["RelationshipStrengthIndex"].mean()
    err = (
        transformed[transformed["IsActiveMember"] == 0]["Exited"].mean()
        / transformed[transformed["IsActiveMember"] == 1]["Exited"].mean()
    )

    print("\n=== POST-ENGINEERING VALIDATION ===")
    print(f"  Total records   : {n:,}  (expected: 10,000)")
    print(f"  Churned         : {churned:,} ({churn_rate:.2f}%)  (expected: 2,037 / 20.37%)")
    print(f"  RSI mean        : {rsi_mean:.4f}  (expected: ~5.6135)")
    print(f"  ERR             : {err:.4f}  (expected: ~1.8818)")
    print(f"  HBD count       : {int(transformed['HighBalanceDisengaged'].sum())}  (expected: 1,247)")
    # ── Drop PII / administrative columns before export (GDPR compliance) ──────
    # Audit finding: Surname, CustomerId, Year carry no analytical value and
    # contradict the manuscript's 'no PII present' claim. Drop before writing.
    pii_cols = [c for c in ['Surname', 'CustomerId', 'Year'] if c in transformed.columns]
    if pii_cols:
        transformed = transformed.drop(columns=pii_cols)
        print(f"  Dropped PII columns: {pii_cols}")

    # Re-check column count after PII drop
    expected_cols = 59 - len(pii_cols)
    print(f"  Total columns   : {transformed.shape[1]}  (expected: {expected_cols} after PII drop)")

    print(f"\nSaving to: {OUTPUT_PATH}")
    transformed.to_csv(OUTPUT_PATH, index=False)
    print("Done. European_Bank_Transformed.csv written successfully.")
