import rasterio
import numpy as np
import pandas as pd
import re
import glob
import os
from sklearn import linear_model
np.warnings.filterwarnings('ignore')


def dir_of_geotiffs_to_dict(target):
    """
    Open and read all geotiifs in a target directory. Raster data stored
    as NumPy arrays in a dictionary. Metadata retained.

    Args:
        target (str): path to directory containing geotiffs

    Returns:
        rstr_dict (dict): dictionary with a key for each GeoTIFF
        Each GeoTIFF key has two sub-keys, "arr" and "meta" that
        store the raster data and metadata.
    Raises:
        Exception: description
    """
    rstr_dict = {}
    file_list = glob.glob(str(target) + '*.tif')

    for f in file_list:
        rstr_dict[f] = {}

        src = rasterio.open(f)
        rstr_dict[f]['arr'] = src.read(1)
        rstr_dict[f]['meta'] = src.meta
        rstr_dict[f]['profile'] = src.profile
        src.close()

    print('%i GeoTIFFs found.' % len(rstr_dict))
    return rstr_dict


def combine_two_dicts(d1, d2):

	d = {**d1, **d2}
	print('%i GeoTIFFs Total.' % len(d))

	return d


def replace_raster_nodata_with_array_nan_for_raster_dict(d):

    for k in d.keys():
        nodata = d[k]['meta']['nodata']
        d[k]['arr'][d[k]['arr'] == nodata] = np.nan
        d[k]['arr'][d[k]['arr'] < 0.0] = np.nan
        d[k]['arr'][d[k]['arr'] > 15.0] = np.nan
    return d


def compute_stats_for_raster_dict(d):

    for k in d.keys():
        d[k]['mu'] = np.nanmean(d[k]['arr']).round(3)
        d[k]['sigma'] = np.nanstd(d[k]['arr']).round(3)
        d[k]['CV'] = (d[k]['sigma'] / d[k]['mu']).round(3)
    return d


def tag_rasters_with_year_data_for_raster_dict(d):

    print("Tag by year...")
    for k in d.keys():
        d[k]['year'] = re.findall('(\d{4})', k)[0]
    return d


def tag_rasters_with_swath_for_raster_dict(d):

    print("Tag by swath...")
    for k in d.keys():
        d[k]['swath'] = k.split('/')[-1].split('_')[0].upper()
    return d


def compute_total_area_for_rasters_in_dict(d):

    print("Computing total area...")
    for k in d.keys():
        pixel_size = d[k]['meta']['transform'][0]
        total_area = (~np.isnan(d[k]['arr'])).sum() * pixel_size
        d[k]['total area m^2'] = total_area
    return d


def compute_total_volume_for_rasters_in_dict(d):

    print("Computing total volume...")
    for k in d.keys():
        pixel_size = d[k]['meta']['transform'][0]
        total_volume = np.nansum(
            (~np.isnan(d[k]['arr'])) * d[k]['arr'] * pixel_size)
        d[k]['total volume m^3'] = total_volume
    return d


def generate_test_thresholds(d, start, stop, increment):
    # Compute test snow depth thresholds.
    # start, e.g. 0.8 = 80% of mean depth,
    # stop, e.g. 2.2 = 220% of mean depth,
    # increment, e.g. 0.1 = test at 10% steps between start and stop

    print("Generating threshold values to test...")
    for k in d.keys():
        d[k]['test thresholds'] = np.round(
            np.arange(start, stop, increment) * d[k]['mu'], 2)
    return d


def compute_area_and_volume_where_depth_exceeds_threshold(d):

    print('Find amount of area and volume that exceeds each threshold...')
    for k in d.keys():

        d[k]['pct. area results'] = []
        d[k]['pct. volume results'] = []
        d[k]['area results m^2'] = []
        d[k]['volume results m^3'] = []

        for thresh in d[k]['test thresholds']:
            print("testing " + str(thresh) + 'm for ' + k)

            # Create sub-dict for each test threshold
            thresh_k = str(thresh) + ' m threshold'
            d[k][thresh_k] = {}

            # Compute binary exceedance mask for each threshold
            drift_mask = (d[k]['arr'] > thresh)

            # Compute snow depth map where mask is 'True' aka depth > threshold
            exceeding_depth_values = drift_mask * d[k]['arr']

            # Set masked out depth values to nan so they can be ignored
            exceeding_depth_values[exceeding_depth_values == 0] = np.nan

            # Compute Area Exceeding Threshold (i.e. count number of pixels), pixel size=1
            d[k][thresh_k]['drift area m^2'] = np.nansum(drift_mask)
            d[k][thresh_k]['pct. drift area'] = (d[k][thresh_k]['drift area m^2'] / d[k]['total area m^2']) * 100
            
            # Compute Volume Exceeding Threshold (i.e. sum of pixel intensities), pixel size=1
            d[k][thresh_k]['drift volume m^3'] = np.nansum(exceeding_depth_values)
            d[k][thresh_k]['pct. drift volume'] = (d[k][thresh_k]['drift volume m^3'] / d[k]['total volume m^3']) * 100
            d[k]['pct. area results'].append(d[k][thresh_k]['pct. drift area'])
            d[k]['pct. volume results'].append(d[k][thresh_k]['pct. drift volume'])
            d[k]['area results m^2'].append(d[k][thresh_k]['drift area m^2'])
            d[k]['volume results m^3'].append(d[k][thresh_k]['drift volume m^3'])
    
    print("Threshold testing complete.")                        
    return d


def compute_pct_volume_pct_area_difference(d):
    
    print('Compute % Volume-Area Difference...')
    for k in d.keys():
        d[k]['pct. volume-area difference'] = [i - j for i, j in zip(d[k]['pct. volume results'],
                                                                     d[k]['pct. area results'])]
    return d
            
def compute_slope_of_pct_volume_pct_area_difference(d):
    
    print('Compute Derivative of % Volume-Area Difference...')
    for k in d.keys():
        d[k]['slope of pct. volume-area difference'] = np.gradient(d[k]['pct. volume-area difference'])
    return d

def find_min_of_slope_of_pct_volume_pct_area_difference(d):
    
    print('Find Minimum of Derivative of % Volume-Area Difference...')
    for k in d.keys():
        d[k]['min. of slope of pct. volume-area difference'] = d[k]['slope of pct. volume-area difference'].min()
        d[k]['index of min. of slope of pct. volume-area difference'] = np.argmin(d[k]['slope of pct. volume-area difference'])
    return d

def find_snowdrift_threshold(d):
    
    print('Use Point of Minimum of Derivative of % Volume-Area Difference to Select Threshold Depth...')
    for k in d.keys():
        d[k]['snowdrift depth threshold m'] = d[k]['test thresholds'][d[k]['index of min. of slope of pct. volume-area difference']]
    return d

def find_snowdrift_areas_and_volumes(d):

    print('Get Drift Area and Volumes at Threshold Depth...')
    for k in d.keys():
        d[k]['pct. snowdrift area'] = d[k]['pct. area results'][d[k]['index of min. of slope of pct. volume-area difference']]
        d[k]['pct. snowdrift volume'] = d[k]['pct. volume results'][d[k]['index of min. of slope of pct. volume-area difference']]
        d[k]['total snowdrift area m^2'] = d[k]['area results m^2'][d[k]['index of min. of slope of pct. volume-area difference']]
        d[k]['total snowdrift volume m^3'] = d[k]['volume results m^3'][d[k]['index of min. of slope of pct. volume-area difference']]
    return d

def compute_area_normalized_drift_volume(d):

    print("Compute Drift Susceptibility...")
    for k in d.keys():
        d[k]['area normalized snowdrift volume m^3/m^2'] = d[k]['total snowdrift volume m^3'] / d[k]['total area m^2']
    return d

def recompute_from_new_threshold(d):

    # assuming user has changed the threshold
    for k in d.keys():
        drift_mask = (d[k]['arr'] > d[k]['snowdrift depth threshold m'])
        # Compute snow depth map where mask is 'True' aka depth > threshold
        exceeding_depth_values = drift_mask * d[k]['arr']
        # Set masked out depth values to nan so they can be ignored
        exceeding_depth_values[exceeding_depth_values == 0] = np.nan
        # Compute Area Exceeding Threshold (i.e. count number of pixels), pixel size=1
        d[k]['total snowdrift area m^2'] = np.nansum(drift_mask)
        d[k]['pct. snowdrift area'] = (d[k]['total snowdrift area m^2'] / d[k]['total area m^2']) * 100
        # Compute Volume Exceeding Threshold (i.e. sum of pixel intensities), pixel size=1
        d[k]['total snowdrift volume m^3'] = np.nansum(exceeding_depth_values)
        d[k]['pct. snowdrift volume'] = (d[k]['total snowdrift volume m^3'] / d[k]['total volume m^3']) * 100
    return d

def dict_to_df(d):
    years = []
    swaths = []
    total_areas = []
    total_volumes = []
    mus = []
    sigmas = []
    drift_depth_thresholds = []
    pct_drift_areas = []
    pct_drift_volumes = []
    total_drift_areas = []
    total_drift_volumes = []
    drift_intensities = []

    for k in d.keys():

        swaths.append(d[k]['swath'])
        years.append(d[k]['year'])
        total_areas.append(d[k]['total area m^2'])
        total_volumes.append(d[k]['total volume m^3'])
        mus.append(d[k]['mu'])
        sigmas.append(d[k]['sigma'])
        drift_depth_thresholds.append(d[k]['snowdrift depth threshold m'])
        pct_drift_areas.append(d[k]['pct. snowdrift area'])
        pct_drift_volumes.append(d[k]['pct. snowdrift volume'])
        total_drift_areas.append(d[k]['total snowdrift area m^2'])
        total_drift_volumes.append(d[k]['total snowdrift volume m^3'])
        drift_intensities.append(d[k]['area normalized snowdrift volume m^3/m^2'])

    df = pd.DataFrame([years, swaths, total_areas, total_volumes, mus, sigmas,
                      drift_depth_thresholds, pct_drift_areas, pct_drift_volumes,
                      total_drift_areas, total_drift_volumes,
                      drift_intensities]).T
    df.columns = ['Year', 'Swath', 'Total Area $m^2$', 'Total Volume $m^3$',
                  'Mean Depth $m$', 'Std. Depth $m$',
                  'Snowdrift Depth Threshold $m$', '%DA', '%DV',
                  'Total Drift Area $m^2$', 'Total Drift Volume $m^3$',
                  'Drift Susceptibility $m$']
    return df


if __name__ == '__main__':
	
	hv_d = dir_of_geotiffs_to_dict('../gis/raster/clpx/snow_depth/corrected/')
	clpx_d = dir_of_geotiffs_to_dict('../gis/raster/hv/snow_depth/corrected/')
	snow_d = combine_two_dicts(hv_d, clpx_d)
	snow_d = replace_raster_nodata_with_array_nan_for_raster_dict(snow_d)
	snow_d = compute_stats_for_raster_dict(snow_d)
	snow_d = tag_rasters_with_year_data_for_raster_dict(snow_d)
	snow_d = tag_rasters_with_swath_for_raster_dict(snow_d)
	snow_d = compute_total_area_for_rasters_in_dict(snow_d)
	snow_d = compute_total_volume_for_rasters_in_dict(snow_d)
	snow_d = generate_test_thresholds(snow_d, 0.8, 2.3, 0.1)
	snow_d = compute_area_and_volume_where_depth_exceeds_threshold(snow_d)
	snow_d = compute_pct_volume_pct_area_difference(snow_d)
	snow_d = compute_slope_of_pct_volume_pct_area_difference(snow_d)
	snow_d = find_min_of_slope_of_pct_volume_pct_area_difference(snow_d)
	snow_d = find_snowdrift_threshold(snow_d)
	snow_d = find_snowdrift_areas_and_volumes(snow_d)
	snow_d = compute_area_normalized_drift_volume(snow_d)

	for k in snow_d.keys():
		print('---')
		print(snow_d[k]['swath'], snow_d[k]['year'])
		print('Total Area: %f km^2' % (snow_d[k]['total area m^2'] / 1000000))
		print('Snowdrift depth threshold: %f m' % snow_d[k]['snowdrift depth threshold m'])
		print('Percent Area Covered by Snowdrift: %f' % snow_d[k]['pct. snowdrift area'])
		print('Percent Volume Stockpiled by Snowdrift: %f' % snow_d[k]['pct. snowdrift volume'])
		print('Drift Susceptibility [m]: %f' % snow_d[k]['area normalized snowdrift volume m^3/m^2'])
		print('---')

	df = dict_to_df(snow_d)
	print("Initial Results: ")
	print(df)

    # This is not an "apples to apples" comparison
	# We are missing the south end of CLPX in 2012 and 2013.
	# How can we account for it?
	# We have the south end in 2015 on...
	# Read them to a dictionary and do same analysis as above...

	clpx_s_dir = '../gis/raster/clpx/snow_depth/corrected/south_end/'
	clpx_s = dir_of_geotiffs_to_dict(clpx_s_dir)
	clpx_s = replace_raster_nodata_with_array_nan_for_raster_dict(clpx_s)
	clpx_s = compute_stats_for_raster_dict(clpx_s)
	clpx_s = tag_rasters_with_year_data_for_raster_dict(clpx_s)
	clpx_s = tag_rasters_with_swath_for_raster_dict(clpx_s)
	clpx_s = compute_total_area_for_rasters_in_dict(clpx_s)
	clpx_s = compute_total_volume_for_rasters_in_dict(clpx_s)
	clpx_s = generate_test_thresholds(clpx_s, 0.8, 2.3, 0.1)
	clpx_s = compute_area_and_volume_where_depth_exceeds_threshold(clpx_s)
	clpx_s = compute_pct_volume_pct_area_difference(clpx_s)
	clpx_s = compute_slope_of_pct_volume_pct_area_difference(clpx_s)
	clpx_s = find_min_of_slope_of_pct_volume_pct_area_difference(clpx_s)
	clpx_s = find_snowdrift_threshold(clpx_s)
	clpx_s = find_snowdrift_areas_and_volumes(clpx_s)
	clpx_s = compute_area_normalized_drift_volume(clpx_s)
	clpx_s_df = dict_to_df(clpx_s)
	clpx_s_df['Swath'] = 'CLPX S.'
	clpx_s_df.sort_values('Year', inplace=True)
	clpx_s_df.set_index('Year', inplace=True)
	print("Results for S. End of CLPX, 2015-2018: ")
	print(clpx_s_df)

	# Replace computed south section thresholds with original threshold from full section
	# Then recompute
	clpx_s[os.path.join(clpx_s_dir, 'clpx_2015_s_end_depth.tif')]['snowdrift depth threshold m'] = 0.77
	clpx_s[os.path.join(clpx_s_dir, 'clpx_2016_s_end_depth.tif')]['snowdrift depth threshold m'] = 0.65
	clpx_s[os.path.join(clpx_s_dir, 'clpx_2017_s_end_depth.tif')]['snowdrift depth threshold m'] = 0.70
	clpx_s[os.path.join(clpx_s_dir, 'clpx_2018_s_end_depth.tif')]['snowdrift depth threshold m'] = 0.81

	clpx_s = recompute_from_new_threshold(clpx_s)
	clpx_s = compute_area_normalized_drift_volume(clpx_s)

	clpx_s_df2 = dict_to_df(clpx_s)
	clpx_s_df2['Swath'] = 'CLPX S.'
	clpx_s_df2.sort_values('Year', inplace=True)
	clpx_s_df2.set_index('Year', inplace=True)

	print(clpx_s_df2)
	# create df for 2015 data onward 
	clpx_2015_on = df.copy(deep=True)[df['Swath'] == 'CLPX']
	clpx_2015_on.sort_values('Year', inplace=True)
	clpx_2015_on = clpx_2015_on.copy(deep=True).iloc[2:]
	clpx_2015_on.set_index('Year', inplace=True)
	clpx_2015_on

	print(clpx_2015_on)

	cols_for_lr = ['Total Area $m^2$', 'Total Drift Area $m^2$',
	               'Total Drift Volume $m^3$', 'Drift Susceptibility $m$',
	               'Mean Depth $m$', 'Std. Depth $m$']

	clpx_full_df_for_lr = clpx_2015_on[cols_for_lr]
	clpx_s_df_for_lr = clpx_s_df2[cols_for_lr]

	clpx_full_df_for_lr.columns = ['Full Total Area $m^2$', 'Full Total Drift Area $m^2$',
	                               'Full Total Drift Volume $m^3$', 'Full Drift Susceptibility $m$',
	                               'Full Mean Depth $m$', 'Full Std. Depth $m$']

	clpx_s_df_for_lr.columns = ['South Total Area $m^2$', 'South Total Drift Area $m^2$',
	                            'South Total Drift Volume $m^3$', 'South Drift Susceptibility $m$',
	                            'South Mean Depth $m$', 'South Std. Depth $m$']

	lr_df = pd.concat([clpx_full_df_for_lr, clpx_s_df_for_lr], axis=1)
	lr_df['Full - South Total Area Difference $m^2$'] = lr_df['Full Total Area $m^2$'] - lr_df['South Total Area $m^2$']
	lr_df['Full - South Drift Volume Difference $m^3$'] = lr_df['Full Total Drift Volume $m^3$'] - lr_df['South Total Drift Volume $m^3$']
	lr_df['Full - South Drift Area Difference $m^2$'] = lr_df['Full Total Drift Area $m^2$'] - lr_df['South Total Drift Area $m^2$']
	lr_df['Full - South Mean Depth Difference $m$'] = lr_df['Full Mean Depth $m$'] - lr_df['South Mean Depth $m$']
	lr_df['Full - South Std. Depth Difference $m$'] = lr_df['Full Std. Depth $m$'] - lr_df['South Std. Depth $m$']

	print(lr_df)

	X = lr_df.copy(deep=True)[['South Total Area $m^2$',
                           'South Total Drift Volume $m^3$',
                           'South Mean Depth $m$',
                           'South Std. Depth $m$']]

	target = pd.DataFrame(lr_df.copy(deep=True), columns=['South Total Drift Volume $m^3$'])
	y = target.copy(deep=True)['South Total Drift Volume $m^3$']

	lm = linear_model.LinearRegression()
	model = lm.fit(X, y)
	predictions = lm.predict(X)

	print(predictions)
	print(lm.score(X, y))
	print(lm.coef_)

	clpx_to_predict = df.copy(deep=True)[df['Swath'] == 'CLPX']
	clpx_to_predict.sort_values('Year', inplace=True)

	clpx_to_predict = clpx_to_predict.copy().iloc[:2]
	clpx_to_predict.set_index('Year', inplace=True)

	# clpx_to_predict_lr = clpx_to_predict[['Total Area $m^2$',
	#                                       'Total Drift Volume $m^3$',]]


	clpx_to_predict_lr = clpx_to_predict[['Total Area $m^2$',
	                                      'Total Drift Volume $m^3$',
	                                      'Mean Depth $m$', 'Std. Depth $m$']]

	clpx_2012_s_drift_volume_prediction, clpx_2013_s_drift_volume_prediction = lm.predict(clpx_to_predict_lr)

	print(clpx_2012_s_drift_volume_prediction)
	print(clpx_2013_s_drift_volume_prediction)

	# Can we also predict the south drift area?

	X = lr_df.copy(deep=True)[['South Total Area $m^2$',
	                           'South Total Drift Area $m^2$',
	                           'South Mean Depth $m$',
	                           'South Std. Depth $m$']]

	target = pd.DataFrame(lr_df.copy(deep=True), columns=['South Total Drift Area $m^2$'])
	y = target.copy(deep=True)['South Total Drift Area $m^2$']

	lm = linear_model.LinearRegression()
	model = lm.fit(X, y)
	predictions = lm.predict(X)

	print(predictions)
	print(lm.score(X, y))
	print(lm.coef_)

	clpx_to_predict = df.copy(deep=True)[df['Swath'] == 'CLPX']
	clpx_to_predict.sort_values('Year', inplace=True)

	clpx_to_predict = clpx_to_predict.copy().iloc[:2]
	clpx_to_predict.set_index('Year', inplace=True)

	# clpx_to_predict_lr = clpx_to_predict[['Total Area $m^2$',
	#                                       'Total Drift Volume $m^3$',]]


	clpx_to_predict_lr = clpx_to_predict[['Total Area $m^2$',
	                                      'Total Drift Area $m^2$',
	                                      'Mean Depth $m$', 'Std. Depth $m$']]

	clpx_2012_s_drift_area_prediction, clpx_2013_s_drift_area_prediction = lm.predict(clpx_to_predict_lr)

	print(clpx_2012_s_drift_area_prediction)
	print(clpx_2013_s_drift_area_prediction)

	# So now we use these predictions to update our original results
	# We need to update the total area measured for CLPX 2012 and 2013
	# We need to update the total volume for CLPX 2012 and 2013
	# To update the total area measured:
	# What is the mean area of the south chunk?
	mean_clpx_s_area = lr_df['South Total Area $m^2$'].mean()
	# print(mean_clpx_s_area)

	# Add this amount (about 16 sq km) to the total area value for clpx in 2012 and 2013

	adjusted_df = df.copy(deep=True)

	# Indexing should be smarter but works for now
	adjusted_df.at[4, 'Total Area $m^2$'] = df.at[4, 'Total Area $m^2$'] + mean_clpx_s_area
	adjusted_df.at[11, 'Total Area $m^2$'] = df.at[11, 'Total Area $m^2$'] + mean_clpx_s_area

	# Now we should do the same with the drift volume predictions
	adjusted_df.at[4, 'Total Drift Volume $m^3$'] = df.at[4, 'Total Drift Volume $m^3$'] + clpx_2012_s_drift_volume_prediction
	adjusted_df.at[11, 'Total Drift Volume $m^3$'] = df.at[11, 'Total Drift Volume $m^3$'] + clpx_2013_s_drift_volume_prediction

	# And now we recompute the drift Susceptibility
	adjusted_df.at[4, 'Drift Susceptibility $m$'] = adjusted_df.at[4, 'Total Drift Volume $m^3$'] / adjusted_df.at[4, 'Total Area $m^2$']
	adjusted_df.at[11, 'Drift Susceptibility $m$'] = adjusted_df.at[11, 'Total Drift Volume $m^3$'] / adjusted_df.at[11, 'Total Area $m^2$']

	# Now we should do the same with the south drift area predictions
	adjusted_df.at[4, 'Total Drift Area $m^2$'] = df.at[4, 'Total Drift Area $m^2$'] + clpx_2012_s_drift_area_prediction
	adjusted_df.at[11, 'Total Drift Area $m^2$'] = df.at[11, 'Total Drift Area $m^2$'] + clpx_2013_s_drift_area_prediction

	print(adjusted_df)

	print(adjusted_df['Drift Susceptibility $m$'] - df['Drift Susceptibility $m$'])

	# Now let us compute drift volume per drift area...this average drift depth
	adjusted_df['Drift Volume / Drift Area (Avg. Drift Depth) $m$'] = adjusted_df['Total Drift Volume $m^3$'] / adjusted_df['Total Drift Area $m^2$']

	adjusted_df.to_csv('results/general_drift_census_results_adjusted.csv')

	# Now let's create masks using the found thresholds for a clpx and hv drift potential map

	hv_profile = snow_d['../gis/raster/hv/snow_depth/corrected/hv_depth_096_2016_corrected_0.00_m.tif']['profile']
	clpx_profile = snow_d['../gis/raster/clpx/snow_depth/corrected/clpx_depth_096_2016_corrected_0.38_m.tif']['profile']

	hvmasks = [snow_d[k]['arr'] > snow_d[k]['snowdrift depth threshold m'] for k in snow_d.keys() if 'hv' in k]
	hv_drift_any_yr = np.logical_or.reduce(hvmasks)
	hv_drift_all_yr = np.logical_and.reduce(hvmasks)
	hv_drift_ct_yr = np.nansum(hvmasks, axis=0)

	clpxmasks = [snow_d[k]['arr'] > snow_d[k]['snowdrift depth threshold m'] for k in snow_d.keys() if 'clpx' in k]
	clpx_drift_any_yr = np.logical_or.reduce(clpxmasks)
	clpx_drift_all_yr = np.logical_and.reduce(clpxmasks)
	clpx_drift_ct_yr = np.nansum(clpxmasks, axis=0)
	
	with rasterio.open('../gis/raster/hv/drift_masks/hv_drift_any_yr.tif', 'w', **hv_profile) as dst:
		dst.write(hv_drift_any_yr.astype('float32'), 1)
	with rasterio.open('../gis/raster/hv/drift_masks/hv_drift_all_yr.tif', 'w', **hv_profile) as dst:
		dst.write(hv_drift_all_yr.astype('float32'), 1)
	with rasterio.open('../gis/raster/hv/drift_masks/hv_drift_count_yr.tif', 'w', **hv_profile) as dst:
		dst.write(hv_drift_ct_yr.astype('float32'), 1)

	with rasterio.open('../gis/raster/clpx/drift_masks/clpx_drift_any_yr.tif', 'w', **clpx_profile) as dst:
		dst.write(clpx_drift_any_yr.astype('float32'), 1)
	with rasterio.open('../gis/raster/clpx/drift_masks/clpx_drift_all_yr.tif', 'w', **clpx_profile) as dst:
		dst.write(clpx_drift_all_yr.astype('float32'), 1)
	with rasterio.open('../gis/raster/clpx/drift_masks/clpx_drift_count_yr.tif', 'w', **clpx_profile) as dst:
		dst.write(clpx_drift_ct_yr.astype('float32'), 1)





