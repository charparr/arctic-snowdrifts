import glob
import os
import re
import rasterio
import numpy as np
import geopandas as gpd
import pandas as pd
import rasterstats as rs

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
        rstr_dict[f] = {}

        src = rasterio.open(f)
        arr = src.read(1, masked=True).filled(np.nan)
        arr[arr <= -9999] = np.nan
        rstr_dict[f]['arr'] = arr
        rstr_dict[f]['mu'] = np.nanmean(rstr_dict[f]['arr'])
        rstr_dict[f]['sigma'] = np.nanstd(rstr_dict[f]['arr'])
        rstr_dict[f]['CV'] = np.divide(rstr_dict[f]['sigma'], rstr_dict[f]['mu'])
        rstr_dict[f]['profile'] = src.profile
        rstr_dict[f]['year'] = re.findall('(\d{4})', f)

    return rstr_dict

# Function to compute zonal raster statistics using rasterstats library
# for single shapefile and many rasters inside a single directory
# Returns geodataframe

def compute_drift_statistics(regx, swath_wildcard, shp):
    d = recursive_rastersstats_to_dict(regx, swath_wildcard)
    geodf = gpd.read_file(shp)
    stats=['mean', 'std', 'median', 'sum']

    for k in d.keys():

        col_name = str(d[k]['year'][0])

        zonal_d = (rs.zonal_stats(geodf, k,
                                 stats=stats))
        geodf[col_name] = zonal_d
        
        for st in stats:
    
            st_series = geodf[col_name].apply(lambda x: x.get(st))
            yr_st_name = col_name + '_' + st
            geodf[yr_st_name] = st_series

        del geodf[col_name]    
    return geodf
    
hv = compute_drift_statistics('../gis/raster/hv/snow_depth/corrected/', '*m.tif', '../gis/vector/drifts/hv_drifts.shp')
clpx = compute_drift_statistics('../gis/raster/clpx/snow_depth/corrected/', '*m.tif', '../gis/vector/drifts/clpx_drifts.shp')
geodf = pd.concat([hv, clpx], sort=False)

geodf.to_csv('results/drift_zonal_stats_all_years.csv')

# Lots of Nans for 2012, 2013
geodf_15on = geodf.dropna(axis=1)

# Get time series averages
all_means = geodf_15on.filter(regex='mean', axis=1)
all_std = geodf_15on.filter(regex='std', axis=1)
all_volumes = geodf_15on.filter(regex='sum', axis=1)
all_meds = geodf_15on.filter(regex='median', axis=1)

ts_mean = all_means.mean(axis=1)
ts_std = all_std.mean(axis=1)
ts_vol = all_volumes.mean(axis=1)
ts_med = all_meds.mean(axis=1)

summary_df = pd.DataFrame()
summary_df['Drift Type'] = geodf_15on.drift_type
summary_df['Study Area'] = [s.upper() for s in geodf_15on.study_area]
summary_df['Drift Area [m^2]'] = geodf_15on.area

summary_df['Mean Drift Depth [m]'] = ts_mean
summary_df['Mean Drift Volume [m^3]'] = ts_vol
summary_df['Std. Drift Depth [m]'] = ts_std
summary_df['Median Drift Depth [m]'] = ts_med

summary_df['CV Drift Depth'] = ts_std / ts_mean
summary_df['Volume:Area Ratio'] = ts_vol / summary_df['Drift Area [m^2]']

summary_df.to_csv('results/drift_zonal_statistics_mean_over_time.csv', index=False)

