import os
from timeit import default_timer as timer
from iqa_metrics import compute_all_iqa, compute_nrmse
from similarity_utils import *

all_base_dirs = ['../../gis/raster/clpx/snow_depth/corrected/fidelity_subsets/clpx_outcrops/',
                 '../../gis/raster/clpx/snow_depth/corrected/fidelity_subsets/clpx_swale/',
                 '../../gis/raster/clpx/snow_depth/corrected/fidelity_subsets/clpx_lake_e/',
                 '../../gis/raster/clpx/snow_depth/corrected/fidelity_subsets/clpx_watertracks_creek/',
                 '../../gis/raster/hv/snow_depth/corrected/fidelity_subsets/hv_lake/',
                 '../../gis/raster/hv/snow_depth/corrected/fidelity_subsets/hv_watertrack/',
                 '../../gis/raster/hv/snow_depth/corrected/fidelity_subsets/hv_stream/',
                 '../../gis/raster/hv/snow_depth/corrected/fidelity_subsets/hv_ice_wedge/'
                 ]

start = timer()

for basedir in all_base_dirs:
    print(basedir.split('/')[-2:])
    #outdir = os.path.join('../results', basedir.split('/')[-2])
    #outf = outdir + '_fidelity_results.csv'

    # Read in raster from data from snow depth maps
    d = rastersstats_to_dict(basedir)

    # Create raster pairs and do similarity analysis on each pair
    pairs = create_pairs(d)
    for p in pairs.keys():
        print('Comparing ' + p + '...')
        ys = [y for y in pairs[p].keys()]
        im1 = pairs[p][ys[0]]['arr']
        im2 = pairs[p][ys[1]]['arr']
        compute_nrmse(im1, im2)

#        pairs[p]['results'] = compute_nrmse(im1, im2)

    #dfs = results_to_dataframe(pairs, outf)

    # # Create Snow Depth Plots, each scene and year
    # #plot_comparison_inputs_stats(d, pltdir)
    # #plot_comparison_inputs_hists(d, pltdir)

    # # Plot IQA maps and save them to disk
    # # for p in pairs.keys():
    #     #plot_iqa_points_on_depth_diff_map(pairs[p], p, pltdir)
    #     #plot_iqa_metric_maps(pairs[p], p, pltdir)
    #     # save_iqa_maps_to_geotiff(pairs[p], p, iqadir)

    # #plot_iqa_scores_from_dfs(dfs, pltdir)

print(str((timer() - start) / 60)[0:4] + ' minutes elapsed')
