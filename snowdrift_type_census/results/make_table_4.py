# Make Table 4: Snowdrift Type Census Zonal Statistics

import pandas as pd

df = pd.read_csv('drift_zonal_statistics_mean_over_time.csv', index_col=False)

del df['Median Drift Depth [m]']

df.replace('watertrack', 'water track (f)', inplace=True)
df.replace('polygon', 'ice wedge (f)', inplace=True)
df.replace('stream', 'stream (nf)', inplace=True)
df.replace('lake', 'lake (nf)', inplace=True)
df.replace('outcrop', 'outcrop (nf)', inplace=True)



df['Drift Area [m^2]'] = df['Drift Area [m^2]'].astype(int)
df['Mean Drift Volume [m^3]'] = df['Mean Drift Volume [m^3]'].astype(int)

df.columns = ['Class','Swath','Drift Area (m<sup>2</sup>)', 'Mean Drift Depth (m)', 'Drift Volume (m<sup>3</sup>)',
			  'Std. Depth (m)', 'CV Depth', 'NDV (m)']



df2 = df.groupby(['Swath','Class']).mean().reset_index()


df2['Drift Area (m<sup>2</sup>)'] = df2['Drift Area (m<sup>2</sup>)'].astype(int)
df2['Drift Volume (m<sup>3</sup>)'] = df2['Drift Volume (m<sup>3</sup>)'].astype(int)

df2.set_index('Swath', inplace=True)
df2 = df2.sort_values('Class')

df2 = df2.round(2)

hv_outcrop = pd.Series(['outcrop (nf)', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',], name='HV', index=df2.columns)
df2 = df2.append(hv_outcrop)
df2 = df2.sort_values('Class')

print(df2.to_markdown())

