import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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


sns.set_context('notebook')
current_palette = sns.color_palette()[0:2][::-1]

ax = sns.scatterplot(x='Class', y='NDV (m)', hue='Swath', style='Swath',
	data=df, palette=current_palette)

plt.axhline(y=1.0, c='r', ls='--', alpha=0.5)
plt.savefig('../../figs/f13_ndv_by_drift_class_300.png', dpi=300, bbox_inches='tight')
plt.savefig('../../figs/f13_ndv_by_drift_class_600.png', dpi=600, bbox_inches='tight')

