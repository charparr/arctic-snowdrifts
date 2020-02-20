import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns

sns.set_context('talk')

df = pd.read_csv('drift_zonal_statistics_mean_over_time.csv', index_col=False)
df.replace('watertrack', 'water track (f)', inplace=True)
df.replace('polygon', 'ice wedge (f)', inplace=True)
df.replace('stream', 'stream (nf)', inplace=True)
df.replace('lake', 'lake (nf)', inplace=True)
df.replace('outcrop', 'outcrop (nf)', inplace=True)

d = {}

for i in df['Drift Type'].unique():

    d[i] = {}
    driftclass = df[df['Drift Type']==i]
    x = driftclass["Drift Area [m^2]"]
    y = driftclass["Mean Drift Volume [m^3]"]
    d[i]['x'] = x
    d[i]['y'] = y
    
    gradient,intercept,r_value,p_value,std_err=stats.linregress(x,y)
    d[i]['Gradient'] = gradient.round(4)
    d[i]['Intercept'] = intercept.round(4)
    d[i]['R Value'] = r_value.round(5)
    d[i]['P Value'] = p_value.round(5)
    d[i]['Std. Error'] = std_err.round(4)

uaclrs = ['#623412', '#A6192E',
          '#65665C', '#719949', '#007681',
          '#D45D00']

linestyles = ['-', ':', '--', '-.', '-', ':']

plt.figure(figsize=(16,10))

i = 0
for k in d.keys():
    lbl = k + " : " + str(d[k]['Gradient'].round(2)) + '$\pm$' + str(d[k]['Std. Error'].round(2))
    x = np.arange(0,100)
    y = d[k]['Gradient'] * x
    plt.plot(x, y, uaclrs[i], ls=linestyles[i], label=lbl, lw=2)
    i+=1

plt.ylabel("Snowdrift Volume $m^3$")
plt.xlabel("Snowdrift Area $m^2$")
leg = plt.legend(loc=2, prop={'size': 20}, frameon=1)
frame = leg.get_frame()
frame.set_facecolor('#EFDBB2')

plt.savefig('../../figs/f15_drift_class_vol_area_regression_300.png',
            dpi=300, bbox_inches='tight')

plt.savefig('../../figs/f15_drift_class_vol_area_regression_600.png',
            dpi=600, bbox_inches='tight')

