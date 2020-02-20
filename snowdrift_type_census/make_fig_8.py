# Make Figure 8: Snowdrift Type Census

import sys
import fiona
import rasterio
import rasterio.plot
import matplotlib as mpl
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import shape, Polygon
from rasterio.windows import Window
import seaborn as sns
from matplotlib_scalebar.scalebar import ScaleBar

sns.set_context('talk')

hv_drift = "../gis/vector/drifts/hv_drifts.shp"
clpx_drift = "../gis/vector/drifts/clpx_drifts.shp"
hv_rstr = '../gis/raster/hv/drift_masks/hv_drift_count_yr.tif'
clpx_rstr = '../gis/raster/clpx/drift_masks/clpx_drift_count_yr.tif'

wt = [hv_drift, 6, hv_rstr, "a.) HV Water Track Drift"]
polycrack  = [clpx_drift, 19, clpx_rstr, "b.) CLPX Ice Wedge Drift"]
stream = [hv_drift, 24, hv_rstr, "c.) HV Stream Drift"]
lake = [clpx_drift, 1, clpx_rstr, "d.) CLPX Lake Drift"]
outcrop = [clpx_drift, 25, clpx_rstr, "e.) CLPX Outcrop Drift"]
other = [hv_drift, 21, hv_rstr, "f.) HV 'Other' Drift"]
drift_plot_info = [wt, polycrack, stream, lake, outcrop, other]

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16,10))
cmap = mpl.cm.get_cmap('Blues', 5)

i = 0
    
while i < len(drift_plot_info):
    
    shp = fiona.open(drift_plot_info[i][0], "r")
    drift_poly = shp[drift_plot_info[i][1]]
    
    drift_bbox = shape(drift_poly['geometry']).bounds
    left = int(drift_bbox[0]) - 25
    bottom = int(drift_bbox[1]) - 25
    right = int(drift_bbox[2]) + 25
    top = int(drift_bbox[3]) + 25
    height = top - bottom
    width = right - left
    
    src = rasterio.open(drift_plot_info[i][2])
    col_skip = abs(src.bounds.left - left)
    row_skip = src.bounds.top - top
    coords = drift_poly['geometry']['coordinates'][0]
    drift = Polygon(coords)
    patches = [PolygonPatch(drift, edgecolor="red", facecolor="none", linewidth=2)]
    
    win = Window(col_skip, row_skip, width, height)

    with rasterio.open(drift_plot_info[i][2]) as src:
        src_transform = src.transform
        win_transform = src.window_transform(win)
        w = src.read(1, window=Window(col_skip, row_skip, width, height))
        if i < 3:
            im = rasterio.plot.show(w/w.max() * 100, transform=win_transform, ax=axes[0][i], cmap=cmap)
            axes[0][i].add_collection(mpl.collections.PatchCollection(patches, match_original=True))
            axes[0][i].set_xticks([])
            axes[0][i].set_yticks([])
            scalebar = ScaleBar(1, box_alpha=0.5) # 1 pixel = 1 meter
            axes[0][i].add_artist(scalebar)
            
        else:
            im = rasterio.plot.show(w/w.max() * 100, transform=win_transform, ax=axes[1][i-3], cmap=cmap)
            axes[1][i-3].add_collection(mpl.collections.PatchCollection(patches, match_original=True))
            axes[1][i-3].set_xticks([])
            axes[1][i-3].set_yticks([])
            scalebar = ScaleBar(1, box_alpha=0.5)
            axes[1][i-3].add_artist(scalebar)
        
        im.set_title(drift_plot_info[i][3], y=1.05)
        
        i += 1
        
cax = fig.add_axes([0.25, 0.01, 0.5, 0.1])
cbar=plt.colorbar(mappable=im.get_children()[-2], cax=cax,
                  ticks = ([0, 20, 40, 60, 80, 100]),
                  orientation='horizontal')

cbar.set_label('% of Winters Classified as Drift')

plt.subplots_adjust(hspace=0.25)
plt.savefig('../figs/f8_snowdrift_types_300.png', dpi=300, bbox_inches='tight')
plt.savefig('../figs/f8_snowdrift_types_600.png', dpi=600, bbox_inches='tight')
