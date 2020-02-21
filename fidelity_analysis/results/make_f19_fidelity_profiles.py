import numpy as np
import matplotlib.pyplot as plt
import rasterio
import pandas as pd
import seaborn as sns
import glob
import os
import re
from scipy.signal import savgol_filter
from skimage.measure import profile_line
import matplotlib.patches as mpatches

def recursive_rastersstats_to_dict(path, fn_regex=r'*2018.tif'):
    """
    Recursively read all rasters in a certain directory and store arrays and
    metadata including statistics in a dicitonary. Filter rasters by suffix or other wildcard.

    Read all GeoTIFFs with rasterio and store values inside an numpy
    array while conserving some metadata inside a dictionary.

    Args:
        path (str): file path to directory containing rasters

    Returns:
        arr (ndarray): array of elevation values
        pixel_size (float): pixel size aka grid/spatial resolution
        profile (dict): metadata profile
    Raises:
        Exception: description
    """

    # Initialize empty dictionary
    rstr_dict = {}
    # Get rasters that in dir and all subdirs that match pattern
    for f in glob.iglob(os.path.join(path, '**', fn_regex), recursive=True):
        
        kf = f.split('/')[-1][:-4]
        if 'v.' in kf:
            kf = kf.split('_')[-2].upper()
        elif 'depth' in kf:
            kf = kf.split('_')[-1] + ' Depth [m]'
        rstr_dict[kf] = {}

        src = rasterio.open(f)
        arr = src.read(1)
        mask = (arr < 0)
        new_array = np.copy(arr)
        arrb = arr + 0.15
        new_array[mask] = arrb[mask]
        rstr_dict[kf]['arr'] = new_array        
        rstr_dict[kf]['mu'] = np.nanmean(rstr_dict[kf]['arr'])
        rstr_dict[kf]['sigma'] = np.nanstd(rstr_dict[kf]['arr'])
        rstr_dict[kf]['CV'] = rstr_dict[kf]['sigma'] / rstr_dict[kf]['mu']
        rstr_dict[kf]['profile'] = src.profile
        rstr_dict[kf]['year'] = re.findall('(\d{4})', f)

    return rstr_dict

clpx_lake = recursive_rastersstats_to_dict('../../../similarity_results/clpx_lake_e/', r'*.tif')

sub = {}

interesting_keys = ['2012 Depth', '2016 Depth', 'dem','NRMSE','SSIM', 'CW-SSIM', 'GMS']
for k in interesting_keys:
    for dk in clpx_lake.keys():
        if k in dk:
            sub[dk]=clpx_lake[dk]
            
del clpx_lake
sub.keys()

# row, col
oblique_src = (420, 640)
oblique_dst = (310, 510)
north_src = (420, 640)
north_dst = (30, 640)



f, axes = plt.subplots(6, 3, gridspec_kw = {'width_ratios':[1, 0.5, 0.75]}, figsize=(16,16))
i = 0

for k in sub.keys():

    # Plot the snow depth and IQA Arrays with annotations
    im = axes[i][0].imshow(sub[k]['arr'], vmin=0, vmax=1, cmap='Blues')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.75)
    axes[i][0].text(0.05, 0.95, k, transform=axes[i][0].transAxes,
                    fontsize=14, verticalalignment='top', bbox=props)

    # Plot the two transect lines over top each array
    oblique_line = profile_line(sub[k]['arr'], oblique_src, oblique_dst)
    north_line = profile_line(sub[k]['arr'], north_src, north_dst)
    
    axes[i][0].plot((north_src[1], north_dst[1]),
                    (north_src[0], north_dst[0]),
                    color='r', lw=3)
    axes[i][0].plot((oblique_src[1], oblique_dst[1]),
                    (oblique_src[0], oblique_dst[0]),
                    color='m', lw=3)
    axes[i][0].plot(oblique_dst[1], oblique_dst[0],
                    color='m', marker=(3,0,45), markersize=9)
    axes[i][0].plot(north_dst[1], north_dst[0],
                    color='r', marker='^', markersize=9)
    
    # Isolate drift chunks using 0.65 m threshold
    if i == 0:
        n12sup_thresh_indices = [idx for idx in range(len(north_line)) if north_line[idx] > 0.65]
        n12sub_thresh_indices = [idx for idx in range(len(north_line)) if north_line[idx] <= 0.65]
        north_drift_start_12 = n12sup_thresh_indices[0]
        north_drift_end_12 = [x for x in n12sub_thresh_indices if x > north_drift_start_12][0]
        #print(north_drift_start_12)
        #print(north_drift_end_12)
        print(len(north_line))
        print(len(oblique_line))
        
        
        o12sup_thresh_indices = [idx for idx in range(len(oblique_line)) if oblique_line[idx] > 0.65]
        o12sub_thresh_indices = [idx for idx in range(len(oblique_line)) if oblique_line[idx] <= 0.65]
        oblique_drift_start_12 = o12sup_thresh_indices[0]
        oblique_drift_end_12 = [x for x in o12sub_thresh_indices if x > oblique_drift_start_12][0]
        #print(oblique_drift_start_12)
        #print(oblique_drift_end_12)
        
    if i == 1:
        n16sup_thresh_indices = [idx for idx in range(len(north_line)) if north_line[idx] > 0.65]
        n16sub_thresh_indices = [idx for idx in range(len(north_line)) if north_line[idx] <= 0.65]
        north_drift_start_16 = n16sup_thresh_indices[0]
        north_drift_end_16 = [x for x in n16sub_thresh_indices if x > north_drift_start_16][0]
        #print(north_drift_start_16)
        #print(north_drift_end_16)
        
        o16sup_thresh_indices = [idx for idx in range(len(oblique_line)) if oblique_line[idx] > 0.65]
        o16sub_thresh_indices = [idx for idx in range(len(oblique_line)) if oblique_line[idx] <= 0.65]
        oblique_drift_start_16 = o16sup_thresh_indices[0]
        oblique_drift_end_16 = [x for x in o16sub_thresh_indices if x > oblique_drift_start_16][0]
        #print(oblique_drift_start_16)
        #print(oblique_drift_end_16)
        
    if i != 5:
        axes[i][0].get_shared_x_axes().join(axes[5][0], axes[i][0])
        axes[i][0].set_yticks([])
        axes[i][0].set_xticks([])
        axes[i][1].get_shared_x_axes().join(axes[5][1], axes[i][1])
        axes[i][1].set_xticks([])
        axes[i][2].get_shared_x_axes().join(axes[5][2], axes[i][2])
        axes[i][2].set_xticks([])
    
    if i > 2:
        axes[i][1].plot(savgol_filter(oblique_line, 3, 1), color='m')
        axes[i][2].plot(savgol_filter(north_line, 3, 1), color='r')
        axes[i][1].yaxis.tick_right()
        axes[i][2].yaxis.tick_right()
    else:
        axes[i][1].plot(oblique_line, color='m')
        axes[i][2].plot(north_line, color='r')
        axes[i][1].yaxis.tick_right()
        axes[i][2].yaxis.tick_right()
    
    if i > 1:
        axes[i][1].set_ylim([0.5, 1.0])
        axes[i][2].set_ylim([0.5, 1.0])
        axes[i][2].set_yticks([0.6, 0.7, 0.8, 0.9, 1.0])
        axes[i][1].axvspan(oblique_drift_start_12, oblique_drift_start_16, alpha=0.33, color='y')
        axes[i][1].axvspan(oblique_drift_end_12, oblique_drift_end_16, alpha=0.33, color='y')
        axes[i][1].axvspan(oblique_drift_start_16, oblique_drift_end_16, alpha=0.33, color='green')
        axes[i][2].axvspan(north_drift_start_12, north_drift_start_16, alpha=0.33, color='y')
        axes[i][2].axvspan(north_drift_end_12, north_drift_end_16, alpha=0.33, color='y')
        axes[i][2].axvspan(north_drift_start_16, north_drift_end_16, alpha=0.33, color='green')
        
        
        
    if i == 5:
        axes[i][1].set_xlabel('Profile Distance [m]')
        axes[i][2].set_xlabel('Profile Distance [m]')
        
    
    
    
    axes[i][1].get_shared_y_axes().join(axes[i][2], axes[i][1])
    axes[i][1].set_yticks([])
    
    i+=1

axes[0][1].axvline(x=oblique_drift_start_12, color='blue', ls='--',
                  label='2012 Drift') 
axes[0][1].axvline(x=oblique_drift_end_12, color='blue', ls='--')
axes[0][2].axvline(x=north_drift_start_12, color='blue', ls='--') 
axes[0][2].axvline(x=north_drift_end_12, color='blue', ls='--')

axes[1][1].axvline(x=oblique_drift_start_16, color='orange', ls='-.',
                  label='2016 Drift') 
axes[1][1].axvline(x=oblique_drift_end_16, color='orange', ls='-.')
axes[1][2].axvline(x=north_drift_start_16, color='orange', ls='-.') 
axes[1][2].axvline(x=north_drift_end_16, color='orange', ls='-.')
axes[0][1].legend()
axes[1][1].legend()

g_patch = mpatches.Patch(color='green', alpha=0.33, label='2012 and 2016 Drift')
y_patch = mpatches.Patch(color='yellow', alpha=0.33, label='Only 2012 Drift')

axes[2][1].legend(handles=[y_patch, g_patch])

f.subplots_adjust(hspace=0, wspace=0)

cbar_ax = f.add_axes([0.4, 0.125, 0.03, 0.65])
f.colorbar(im, cax=cbar_ax, orientation='vertical')

plt.savefig('drift_scour_fidelity_fig.png', dpi=200, bbox_inches='tight')
