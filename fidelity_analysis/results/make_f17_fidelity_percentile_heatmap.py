import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_context('talk')

spal = sns.diverging_palette(245, 64, s=87, l=84)



df = pd.read_csv('all_fidelity_results.csv')

print(df.head())

df.columns = ['NRMSE', 'SSIM', 'CW-SSIM', 'GMS', 'Class', 'Swath', 'Winters Compared']
df.replace({'swale': "Other", 'ice': "Ice Wedge",
	'watertrack': "Water track", 'watertracks': "Water track", 'outcrops': 'Outcrop',
	'lake': 'Lake', 'stream': 'Stream'}, inplace=True)

df['Avg. Fidelity Score'] = df[['NRMSE', 'SSIM', 'CW-SSIM', 'GMS']].mean(axis=1)
df['Swath and Drift Class'] = df['Swath'] + ' ' + df['Class']

print(df.head())

rdf = df.copy()
rdf['NRMSE Rank'] = rdf.NRMSE.rank(pct=True).round(3) * 100
rdf['SSIM Rank'] = rdf.SSIM.rank(pct=True).round(3) * 100
rdf['CW-SSIM Rank'] = rdf['CW-SSIM'].rank(pct=True).round(3) * 100
rdf['GMS Rank'] = rdf.GMS.rank(pct=True).round(3) * 100
rdf['Avg. Similarity Rank'] = rdf[['NRMSE Rank', 'SSIM Rank',
                                   'CW-SSIM Rank', 'GMS Rank']].mean(axis=1)
#rdf['Swath and Drift Class'] = rdf['Swath'] + ' ' + rdf['Drift Class']
print(rdf.head())

mean_ranks = rdf.pivot("Swath and Drift Class", "Winters Compared", "Avg. Similarity Rank")
print(mean_ranks.head())

fig, ax = plt.subplots(figsize=(16,9))
sns.heatmap(mean_ranks, ax=ax, annot=True, square=True,
            cmap=spal, center=50, vmin=0, vmax=100,
            linewidths=.5)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
ax.set_title("Average Fidelity Percentile")

plt.savefig('../../figs/f17_fidelity_heatmap_300.png',
	dpi=300, bbox_inches='tight')

plt.savefig('../../figs/f17_fidelity_heatmap_600.png',
	dpi=600, bbox_inches='tight')