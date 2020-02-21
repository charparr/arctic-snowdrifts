
import pandas as pd
pd.set_option('precision', 3)

df = pd.read_csv('all_fidelity_results.csv')

df2 = df.groupby(['Swath']).mean()
df2['Avg.'] = df2.mean(numeric_only=True, axis=1)

df2.columns = ['NRMSE', 'SSIM', 'CW-SSIM', 'GMS', 'Avg.']

df2 = df2.round(2)

print(df2.to_markdown())
