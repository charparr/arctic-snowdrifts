#!/usr/bin/env python

import argparse
import geopandas as gpd
import rasterio
import pandas as pd
import numpy as np
from os.path import basename, dirname, join


parser = argparse.ArgumentParser(description='Utility to perform validation of airborne lidar or airborne SfM generated snow depth surfaces. This tool compares a set of MagnaProbe snow depth measurments to the value of the snow depth raster at the same location. This tool can also write a new raster that is adjusted by the mean difference between the probe depth and raster value, write the validation results to shapefile and csv, and generate plots.')

parser.add_argument("-shp", "--magna_shp", help="Path MangaProbe shapefile of validation points.csv")
parser.add_argument("-dDEM", "--depth_dDEM", help="depth dDEM raster to validate")
parser.add_argument("-outrstr", "--output_tif", type=bool, default=False, help="write a corrected depth dDEM output raster?")
parser.add_argument("-out_results", "--output_results", type=bool, default=False, help="write validation results to shapefile and .csv?")
args = parser.parse_args()

# Read and prep validation points
probes = gpd.read_file(args.magna_shp)
probes = probes[['UTM_E', 'UTM_N', 'Depth_m', 'geometry']]
probes.dropna(inplace=True)
probes.index = range(len(probes))
coords = [(x,y) for x, y in zip(probes.UTM_E, probes.UTM_N)]

# Open the depth DEM and store metadata
src = rasterio.open(args.depth_dDEM)
profile = src.profile

# Sample the raster at every probe location and store values in DataFrame
probes['Raster Value [m]'] = [x for x in src.sample(coords)]
probes['Raster Value [m]'] = probes.apply(lambda x: x['Raster Value [m]'][0], axis=1)
probes = probes[probes['Raster Value [m]'] != -9999]
probes['Probe-Raster Delta [m]'] = probes['Depth_m'] - probes['Raster Value [m]']

mean_offset = round(probes['Probe-Raster Delta [m]'].mean(),2)
sigma = round(probes['Probe-Raster Delta [m]'].std(),2)
probes['Raster Value Corrected [m]'] = probes['Raster Value [m]'] + mean_offset


if args.output_tif == True:
    # Generate raster destination in appropriate 'corrected' depth_dDEM dir
    out_dest = join(dirname(dirname(args.depth_dDEM)), 'corrected')
    out_prefix = basename(args.depth_dDEM).split('.')[0]
    out_suffix = "_corrected_" + str(mean_offset) + '_m.tif'
    out_path_corr = join(out_dest, out_prefix + out_suffix)

    # apply correction to depth map (except in NoData areas)
    depth_array = src.read(1)
    if mean_offset < 0:
    	depth_array[depth_array != -9999] -= mean_offset
    else:
    	depth_array[depth_array != -9999] += mean_offset
    depth_array[np.where(np.logical_and(depth_array > -9998, depth_array < 0))] = 0

    print ('Writing snow depth raster. Correction value: ' + str(mean_offset) + ', destination is ' + str(out_path_corr))
    with rasterio.open(out_path_corr, 'w', **profile) as dst:
        dst.write(depth_array, 1)
    print ('Corrected raster creation complete.')
else:
    print('Skipping creation of corrected raster...')

if args.output_results:
    print('Writing results .shp and .csv...')
    # Generate .shp/.csv destination in appropriate results folder
    out_prefix = basename(args.magna_shp).split('.')[0]
    out_suffix = '_validation_results'
    out_path = join('results', out_prefix + out_suffix)
    print(out_path)
    geo_probes = gpd.GeoDataFrame(probes, crs={'init': 'epsg:32606'})
    geo_probes.to_file(out_path + '.shp')
    probes.to_csv(out_path + '.csv', index=False)
else:
    print('Skipping creation of validation results file...')

print("Validation process is complete.")
