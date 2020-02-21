import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context('talk')

n = gpd.read_file('../gis/vector/magnaprobes/hv/2017/watertracks/hv_2017_water_track_N_transects.shp')
s = gpd.read_file('../gis/vector/magnaprobes/hv/2017/watertracks/hv_2017_water_track_s_transects.shp')

plt.figure(figsize=(21,8))
plt.plot(n['UTM_E'], n['Depth_m'], color='pink', lw=3)
plt.plot(s['UTM_E'], s['Depth_m'], color='green', lw=3)
plt.ylabel('Snow Depth (m)')
plt.xlabel('UTM E')
plt.savefig('n_wt.png', dpi=1600, bbox_inches='tight')
