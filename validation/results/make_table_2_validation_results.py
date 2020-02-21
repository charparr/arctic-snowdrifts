
import os
import fnmatch
import pandas as pd

print('Aggregating validation results...')

from os import listdir

def find_csv_filenames( path_to_dir, suffix="results.csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

res = find_csv_filenames('.')

years = ['2012', '2013', '2015', '2016', '2017', '2018']
store_stats = []
for filename in res:
    print(filename)
    if 'clpx' in filename:
        domain = 'CLPX'
    elif 'hv' in filename:
        domain = 'HV'
    for y in years:
        if y in filename:
            year = y
    val_stats = pd.read_csv(filename)
    val_stats['Year'] = year
    val_stats['Swath'] = domain
    store_stats.append(val_stats)

master_df = pd.concat(store_stats)
#master_df.to_csv('aggregate_results/aggregate_validation_results_all.csv')

table2 = master_df[['Year','Swath','Probe-Raster Delta [m]']]

table2['Swath and Year'] = table2['Swath'] + ' ' + table2['Year']
df = table2.groupby('Swath and Year').mean().round(2)
df['Count'] = table2.groupby('Swath and Year').count()['Year'].astype(int)
df['Std. (m)'] = table2.groupby('Swath and Year').std().round(2)

print(df)
df['Year'] = [2012,2013,2015,2016,2017,2018,2012,2013,2015,2017,2018]
df['Swath'] = ['CLPX','CLPX','CLPX','CLPX','CLPX','CLPX', 'HV', 'HV', 'HV', 'HV', 'HV']

df.rename(columns={'Probe-Raster Delta [m]':'Mean (m)'}, inplace=True)
df = df[['Year', 'Swath', 'Count', 'Mean (m)', 'Std. (m)']]


mean_row = pd.Series(['', '', int(df.Count.astype(float).mean()), df['Mean (m)'].mean().round(2), df['Std. (m)'].mean().round(2)], name='Mean', index=df.columns)
total_row = pd.Series(['', '', int(df.Count.astype(float).sum()), '', ''], name='Total', index=df.columns)

narow = pd.Series([2016, 'HV', 'N/A', 'N/A', 'N/A'], name='HV 2016', index=df.columns)
df = df.append(narow)
df = df.sort_values('Year')

df = df.append(mean_row)
df = df.append(total_row)

df.set_index('Year', inplace=True)

as_list = df.index.tolist()
idx = as_list.index('')
as_list[idx] = 'Mean'
idx = as_list.index('')
as_list[idx] = 'Total'
df.index = as_list
df.index.name = 'Year'

print(df.to_markdown())





