import os
from timeit import default_timer as timer
from iqa_metrics import compute_all_iqa
from similarity_utils import *

#all_base_dirs = ['../../gis/raster/hv/snow_depth/corrected/kidney_lake/']

all_base_dirs = ['../../gis/raster/clpx/snow_depth/corrected/fidelity_subsets/clpx_outcrops/']


start = timer()

for basedir in all_base_dirs:
    
    outdir = os.path.join('../results', basedir.split('/')[-2])
    outf = outdir + '_fidelity_results.csv'

    # Read in raster from data from snow depth maps
    d = rastersstats_to_dict(basedir)

    # Create raster pairs and do similarity analysis on each pair
    pairs = create_pairs(d)
    for p in pairs.keys():
        print('Comparing ' + p + '...')
        ys = [y for y in pairs[p].keys()]
        im1 = pairs[p][ys[0]]['arr']
        im2 = pairs[p][ys[1]]['arr']
        pairs[p]['results'] = compute_all_iqa(im1, im2)

    dfs = results_to_dataframe(pairs, outf)

    # # Create Snow Depth Plots, each scene and year
    # #plot_comparison_inputs_stats(d, pltdir)
    # #plot_comparison_inputs_hists(d, pltdir)

    # # Plot IQA maps and save them to disk
    for p in pairs.keys():
        save_iqa_maps_to_geotiff(pairs[p], p, '../results/clpx_outcrops/')

    # #plot_iqa_scores_from_dfs(dfs, pltdir)

print(str((timer() - start) / 60)[0:4] + ' minutes elapsed')
