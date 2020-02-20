
import rasterio
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def rastersstats_to_dict(dir):

    rstr_dict = {}

    file_list = glob.glob(str(dir) + '*.tif')

    for f in file_list:

        rstr_dict[f] = {}

        src = rasterio.open(f)
        rstr_dict[f]['arr'] = src.read(1)
        rstr_dict[f]['mu'] = np.nanmean(rstr_dict[f]['arr'])
        rstr_dict[f]['sigma'] = np.nanstd(rstr_dict[f]['arr'])
        rstr_dict[f]['CV'] = rstr_dict[f]['sigma'] / rstr_dict[f]['mu']
        rstr_dict[f]['year'] = re.findall('(\d{4})', f)

    return rstr_dict


d = rastersstats_to_dict('../gis/raster/hv/snow_depth/corrected/fidelity_subsets/hv_watertrack/')

arrs = []
yrs = []
for k in d.keys():
    arrs.append(d[k]['arr'])
    yrs.append(d[k]['year'][0])

fig, axes = plt.subplots(figsize=(9, 9), nrows=3, ncols=2)

i=0

for y, a, ax in sorted(zip(yrs, arrs, axes.flat), key = lambda x: x[0]):

    im = ax.imshow(a, cmap='Spectral',
        interpolation='nearest', vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(y)

    # inset axes....
    axins = ax.inset_axes([0.65, 0.65, 0.32, 0.32])
    axins.imshow(a, cmap='Spectral',
        interpolation='lanczos', vmin=0, vmax=1)
    # sub region of the original image
    x1, x2, y1, y2 = 425, 450, 200, 225
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xticks([])
    axins.set_yticks([])
    [i.set_linewidth(2.0) for i in axins.spines.values()]
    
    #ax.indicate_inset_zoom(axins, ec='k')
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="k", lw=1)

    if i == 0:
        scalebar = ScaleBar(1, box_alpha=0.5, location=2) # 1 pixel = 1 meter
        scalebar2 = ScaleBar(1, box_alpha=0.33, height_fraction=0.06, length_fraction=0.4) # 1 pixel = 1 meter
        ax.add_artist(scalebar)
        axins.add_artist(scalebar2)
    i += 1

cax = fig.add_axes([0.25, 0.01, 0.5, 0.06])
cbar=plt.colorbar(mappable=im, cax=cax,
                  ticks = ([0, 0.2, 0.4, 0.6, 0.8, 1.0]),
                  orientation='horizontal')

cbar.set_label('Snow Depth (m)')
cbar.ax.set_xticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '>1.0'])

plt.subplots_adjust(wspace=0.0)


plt.savefig('../figs/f16_pattern_fidelity_300.png', bbox_inches='tight', dpi=300)

plt.savefig('../figs/f16_pattern_fidelity_600.png', bbox_inches='tight', dpi=600)



# src = rasterio.open(args.raster)
# arr = src.read(1)

# masked_arr = np.ma.masked_values(arr, src.nodata)
# dmin = np.min(masked_arr)
# dmax = np.max(masked_arr)
# mu = np.mean(masked_arr)
# sigma = np.std(masked_arr)

# # Init. plot properties
# if args.cmap:
#     cmap = plt.get_cmap(args.cmap)
# else:
#     cmap = plt.get_cmap('Spectral')
# cmap.set_under('white')  # Color for values less than vmin
# xaxlabel = 'UTM E Zone ' + args.utm + ' N'
# yaxlabel = 'UTM N Zone ' + args.utm + ' N'
# fig_x = int(10 * src.meta['width'] / src.meta['height'])
# fig_y = int(10 * src.meta['height'] / src.meta['width'])
# if fig_y > fig_x:
#     fig_x += 2
# textstr = '$\mu=%.2f$\n$\sigma=%.2f$\nmin = %.2f\nmax = %.2f' % (mu, sigma, dmin, dmax)

# # Create figure
# fig, ax = plt.subplots(figsize=(fig_x, fig_y))
# ax.set_title(args.title)
# ax.set_ylabel(xaxlabel)
# ax.set_xlabel(yaxlabel)
# # place a text box in upper left in axes coords
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.66)
# if fig_y > fig_x:
#     ax.text(0.05, 0.15, textstr, transform=ax.transAxes, fontsize=14,
#     verticalalignment='top', bbox=props)
# else:
#     ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
#     verticalalignment='top', bbox=props)

# show((src, 1), with_bounds=True, ax=ax, vmin=args.vmin, vmax=args.vmax, cmap=cmap)
# plt.setp( ax.xaxis.get_majorticklabels(), rotation=45 )
# PCM=ax.get_children()[-2]
# plt.colorbar(PCM, ax=ax)
# plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
