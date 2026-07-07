import pandas as pd
import numpy as np
import warnings, os
warnings.filterwarnings('ignore')

# Use a path relative to the script file to make the project portable
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'European_Bank_Transformed.csv')
df = pd.read_csv(DATA_PATH)


print('=== MASTER STATS FOR RESEARCH PAPER ===')
n = len(df)
churned = df['Exited'].sum()
retained = n - churned
churn_rate = df['Exited'].mean() * 100
print(f'Total customers: {n:,}')
print(f'Churned: {churned:,} ({churn_rate:.2f}%)')
print(f'Retained: {retained:,} ({100-churn_rate:.2f}%)')

print('\n--- Geography ---')
geo = df.groupby('Geography').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean')).round(4)
print(geo)

print('\n--- Gender ---')
gen = df.groupby('Gender').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean')).round(4)
print(gen)

print('\n--- IsActiveMember ---')
act = df.groupby('IsActiveMember').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean')).round(4)
print(act)
active_churn = df[df['IsActiveMember']==1]['Exited'].mean()
inactive_churn = df[df['IsActiveMember']==0]['Exited'].mean()
print(f'ERR ratio (inactive/active): {inactive_churn/active_churn:.4f}')

print('\n--- NumOfProducts ---')
prod = df.groupby('NumOfProducts').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean')).round(4)
print(prod)

print('\n--- HasCrCard ---')
cc = df.groupby('HasCrCard').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean')).round(4)
print(cc)

print('\n--- EngagementTier ---')
eng = df.groupby('EngagementTier').agg(
    Count=('Exited','count'),
    Churned=('Exited','sum'),
    ChurnRate=('Exited','mean'),
    AvgBalance=('Balance','mean'),
    AvgSalary=('EstimatedSalary','mean'),
    AvgProducts=('NumOfProducts','mean'),
    AvgRSI=('RelationshipStrengthIndex','mean')
).round(2)
print(eng)

print('\n--- RSI Band ---')
rsi = df.groupby('RSI_Band').agg(Count=('Exited','count'), Churned=('Exited','sum'), ChurnRate=('Exited','mean'), AvgRSI=('RelationshipStrengthIndex','mean')).round(4)
print(rsi)

print('\n--- AgeBand ---')
age_g = df.groupby('AgeBand').agg(Count=('Exited','count'), ChurnRate=('Exited','mean')).round(4)
print(age_g)

print('\n--- Balance stats ---')
mean_bal = df['Balance'].mean()
std_bal = df['Balance'].std()
zero_bal = (df['Balance']==0).sum()
zero_bal_pct = (df['Balance']==0).mean()*100
zero_churn = df[df['Balance']==0]['Exited'].mean()*100
nonzero_churn = df[df['Balance']>0]['Exited'].mean()*100
print(f'Mean balance: {mean_bal:.2f}')
print(f'Std balance: {std_bal:.2f}')
print(f'Zero balance customers: {zero_bal:,} ({zero_bal_pct:.2f}%)')
print(f'Churn rate zero balance: {zero_churn:.2f}%')
print(f'Churn rate non-zero balance: {nonzero_churn:.2f}%')

print('\n--- KPIs ---')
prem = df['IsPremiumCustomer'].sum()
prem_churn = df[df['IsPremiumCustomer']==1]['Exited'].mean()*100
hbd = df['HighBalanceDisengaged'].sum()
hbd_churn = df[df['HighBalanceDisengaged']==1]['Exited'].mean()*100
sticky = df['IsStickyCustomer'].sum()
sticky_churn = df[df['IsStickyCustomer']==1]['Exited'].mean()*100
silent = df['SilentChurnRisk'].sum()
silent_churn = df[df['SilentChurnRisk']==1]['Exited'].mean()*100
mismatch = df['SalaryBalanceMismatch'].sum()
mismatch_churn = df[df['SalaryBalanceMismatch']==1]['Exited'].mean()*100
wealth_gap = df['WealthEngagementGap'].sum()
print(f'Premium Customers (top 25% balance): {prem:,}')
print(f'Premium Customer churn rate: {prem_churn:.2f}%')
print(f'High-Balance Disengaged: {hbd:,} ({hbd/n*100:.2f}%)')
print(f'High-Balance Disengaged churn: {hbd_churn:.2f}%')
print(f'Sticky Customers: {sticky:,} ({sticky/n*100:.2f}%)')
print(f'Sticky Customer churn rate: {sticky_churn:.2f}%')
print(f'Silent Churn Risk: {silent:,}')
print(f'Silent churn rate: {silent_churn:.2f}%')
print(f'Salary-Balance Mismatch: {mismatch:,}')
print(f'Mismatch churn rate: {mismatch_churn:.2f}%')
print(f'Wealth Engagement Gap: {wealth_gap:,}')

print('\n--- CreditScore ---')
cs_mean = df['CreditScore'].mean()
cs_churn = df[df['Exited']==1]['CreditScore'].mean()
cs_retain = df[df['Exited']==0]['CreditScore'].mean()
print(f'Mean CreditScore: {cs_mean:.2f}')
print(f'CreditScore churned: {cs_churn:.2f}')
print(f'CreditScore retained: {cs_retain:.2f}')

print('\n--- Tenure ---')
ten_mean = df['Tenure'].mean()
ten_churn = df[df['Exited']==1]['Tenure'].mean()
ten_retain = df[df['Exited']==0]['Tenure'].mean()
print(f'Mean Tenure: {ten_mean:.2f}')
print(f'Tenure churned: {ten_churn:.2f}')
print(f'Tenure retained: {ten_retain:.2f}')

print('\n--- Age ---')
age_mean = df['Age'].mean()
age_churn = df[df['Exited']==1]['Age'].mean()
age_retain = df[df['Exited']==0]['Age'].mean()
print(f'Mean Age: {age_mean:.2f}')
print(f'Age churned: {age_churn:.2f}')
print(f'Age retained: {age_retain:.2f}')

print('\n--- Salary ---')
sal_mean = df['EstimatedSalary'].mean()
sal_churn = df[df['Exited']==1]['EstimatedSalary'].mean()
sal_retain = df[df['Exited']==0]['EstimatedSalary'].mean()
print(f'Mean salary: {sal_mean:.2f}')
print(f'Salary churned: {sal_churn:.2f}')
print(f'Salary retained: {sal_retain:.2f}')

print('\n--- ProductBreadth ---')
pb = df.groupby('ProductBreadth').agg(Count=('Exited','count'), ChurnRate=('Exited','mean'), AvgBalance=('Balance','mean')).round(4)
print(pb)

print('\n--- RiskBand ---')
rb = df.groupby('RiskBand').agg(Count=('Exited','count'), ActualChurn=('Exited','mean')).round(4)
print(rb)

print('\n--- TenureSegment ---')
ts = df.groupby('TenureSegment').agg(Count=('Exited','count'), ChurnRate=('Exited','mean')).round(4)
print(ts)

print('\n--- Multi-product detail ---')
sp = (df['NumOfProducts']==1).sum()
sp_churn = df[df['NumOfProducts']==1]['Exited'].mean()*100
mp = (df['NumOfProducts']>=2).sum()
mp_churn = df[df['NumOfProducts']>=2]['Exited'].mean()*100
amp = df['ActiveAndMultiProduct'].sum()
amp_churn = df[df['ActiveAndMultiProduct']==1]['Exited'].mean()*100
isp = df['InactiveAndSingleProduct'].sum()
isp_churn = df[df['InactiveAndSingleProduct']==1]['Exited'].mean()*100
print(f'Single product customers: {sp:,}')
print(f'Single product churn: {sp_churn:.2f}%')
print(f'Multi product customers: {mp:,}')
print(f'Multi product churn: {mp_churn:.2f}%')
print(f'Active+MultiProduct count: {amp:,}')
print(f'Active+MultiProduct churn: {amp_churn:.2f}%')
print(f'Inactive+SingleProduct count: {isp:,}')
print(f'Inactive+SingleProduct churn: {isp_churn:.2f}%')

print('\n--- BalanceTier churn ---')
bt = df.groupby('BalanceTier').agg(Count=('Exited','count'), ChurnRate=('Exited','mean')).round(4)
print(bt)

print('\n--- CreditTier churn ---')
ct = df.groupby('CreditTier').agg(Count=('Exited','count'), ChurnRate=('Exited','mean')).round(4)
print(ct)

print('\n--- Correlation with Exited ---')
num_cols = ['CreditScore','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','RelationshipStrengthIndex','RetentionRiskScore']
corrs = df[num_cols + ['Exited']].corr()['Exited'].drop('Exited').sort_values()
print(corrs.round(4))
