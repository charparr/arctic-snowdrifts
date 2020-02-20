# Make Figure 7 from Data in Table 3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context('talk')

df = pd.read_csv('general_drift_census_results_adjusted.csv')

fig = plt.figure(figsize=(12,12))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharey = ax1)
ax3 = fig.add_subplot(223, sharex = ax1)
ax4 = fig.add_subplot(224, sharey = ax3, sharex=ax2)

sns.boxplot(x="Swath", y='Drift Susceptibility $m$',
            data=df, ax=ax1)

sns.pointplot(x="Year", y="Drift Susceptibility $m$",
                hue="Swath", data=df, ax=ax2, markers=["o", "x"])

sns.boxplot(x="Swath", y='Drift Volume / Drift Area (Avg. Drift Depth) $m$',
            data=df, ax=ax3)

sns.pointplot(x="Year", y='Drift Volume / Drift Area (Avg. Drift Depth) $m$',
                hue="Swath", data=df, ax=ax4, markers=["o", "x"])

ax1.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
ax2.xaxis.set_visible(False)
ax4.yaxis.set_visible(False)

# Close the FacetGrid figure which we don't need (g.fig)
fig.subplots_adjust(wspace=0)
fig.subplots_adjust(wspace=0,hspace=0)

plt.savefig('../../figs/f7_general_census_4panel_300.png',
            dpi=300, bbox_inches='tight')

plt.savefig('../../figs/f7_general_census_4panel_600.png',
            dpi=600, bbox_inches='tight')
