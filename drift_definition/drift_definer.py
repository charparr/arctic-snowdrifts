
import argparse
import rasterio
import numpy  as np
import pandas as pd

np.seterr(invalid='ignore')


'''
This is a script to compute a snow depth threshold beyond which we are confident a snowdrift is present.
This tool computes the areal fraction and volume of drift vs. not-drift (i.e. veneer or scoured) snow for a range of snow depth thresholds.
Tool uses that information to converge on a single threshold value.
'''

parser = argparse.ArgumentParser(description='A tool to plot drift areal fraction / volume vs. depth threshold (percent of mean snow depth).')
parser.add_argument("-d", "--depth_dDEM", help="Snow Depth dDEM")
args = parser.parse_args()

# Open the snow depth map and read to array.
src = rasterio.open(args.depth_dDEM)
depth = src.read(1)
depth[depth == src.meta['nodata']] = np.nan
depth[depth < 0] = np.nan
depth[depth >= 10.0] = np.nan

# Compute some basic statistics
mean_depth = np.nanmean(depth)
std_depth = np.nanstd(depth)
cv_depth = std_depth / mean_depth

# depth thresholds (percentages of mean depth) to test 
thresholds = np.round(np.arange(0.8, 2.1, 0.05) * mean_depth, 2)

# Computing total area / volume of all snow pixels
pxl_sz = src.meta['transform'][0]
total_area = (~np.isnan(depth)).sum() * pxl_sz
total_volume = np.nansum((~np.isnan(depth)) * depth * pxl_sz)
print(pxl_sz)
print(total_area)
print(total_volume)

# Setting some result tags based on year and study area, based on input map
if 'mean' in args.depth_dDEM:
    year = 'Mean_Depth'
else:
    year = [s for s in args.depth_dDEM[:-4].split('_') if s.isdigit()][-1]

if 'clpx' in args.depth_dDEM.lower():
    study_area = 'CLPX'
    mtn = '' # was for tulomne, but keep in case of subsets of hv/clpx
elif 'hv' in args.depth_dDEM.lower():
    study_area = 'HV'
    mtn = ''

print('Computing snowdrift threshold for ' + study_area + ': ' + year + mtn)

# Compute depth thresholds
# Results stored in nested dict, keys are depth and results for that depth
d = dict()

for i in thresholds:

    k = str(i) + ' m'
    print('testing threshold of ' + k + '...')

    drift_mask = (depth >= i)
    depth_drift_masked = drift_mask * depth
    depth_drift_masked[depth_drift_masked == 0] = np.nan
    not_drift_mask = (depth < i)
    depth_not_drift_masked = not_drift_mask * depth
    depth_not_drift_masked[depth_not_drift_masked == 0] = np.nan

    d[k] = {}
    d[k]['drift_area'] = int(np.nansum(drift_mask))
    d[k]['not_drift_area'] = int(np.nansum(not_drift_mask))
    d[k]['drift_volume'] = int(np.nansum(drift_mask * depth * pxl_sz))
    d[k]['not_drift_volume'] = int(np.nansum(not_drift_mask * depth * pxl_sz))
    d[k]['mean_drift_depth'] = np.nanmean(depth_drift_masked)
    d[k]['mean_not_drift_depth'] = np.nanmean(depth_not_drift_masked)

# Move to dict to df for output and analysis
df = pd.DataFrame.from_dict(d).T
df['Drift Threshold (pct. of mean depth)'] = np.arange(0.8, 2.1, 0.05) * 100
df['Drift Area pct.'] = df.drift_area / total_area * 100
df['Not Drift Area pct.'] = df.not_drift_area / total_area * 100
df['Drift Volume pct.'] = df.drift_volume / total_volume * 100
df['Not Drift Volume pct.'] = df.not_drift_volume / total_volume * 100
df['Drift Volume-Area Difference (pct.)'] = df['Drift Volume pct.'] - df['Drift Area pct.']

df['Drift Volume-Area Difference Slope'] = np.gradient(df['Drift Volume-Area Difference (pct.)'])

if year == 'Mean_Depth':
    df['Year'] = 'Mean_Depth'
else:
    df['Year'] = int(year)
df['Study Area'] = study_area

# Find the inflection Threshold
df.set_index(df['Drift Threshold (pct. of mean depth)'], inplace=True)
inflection = df['Drift Volume-Area Difference Slope'].idxmin()
df['Inflection Threshold'] = inflection
df['Mean_Depth [m]'] = mean_depth
df['SD Depth [m]'] = std_depth
df['CV'] = cv_depth
df['Total Area'] = total_area
df['Total Volume'] = total_volume

df.to_csv('results/drift_thresholds_' + mtn + study_area +'_' + year + '.csv')
