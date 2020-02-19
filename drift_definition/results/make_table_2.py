import pandas as pd

df = pd.read_csv('general_drift_census_results_adjusted.csv')

df2 = df[['Year', 'Swath','Mean Depth $m$', 'Snowdrift Depth Threshold $m$',
       '%DA', '%DV', 'Total Drift Area $m^2$', 'Total Drift Volume $m^3$',
       'Drift Susceptibility $m$',
       'Drift Volume / Drift Area (Avg. Drift Depth) $m$']]

df2.columns = ['Year', 'Swath', 'Mean Depth (m)',
			   'Depth Threshold (m)', '%DA', '%DV',
			   'Total Drift Area (m<sup>2</sup>)','Total Drift Volume (m<sup>3</sup>)',
			   'Drift Susceptibility (m)', 'Mean Drift Depth (m)']

df2.sort_values('Year', inplace=True)

df2['%DA'] = df2['%DA'].round(2)
df2['%DV'] = df2['%DV'].round(2)
df2['Drift Susceptibility (m)'] = df2['Drift Susceptibility (m)'].round(2)
df2['Mean Depth (m)'] = df2['Mean Depth (m)'].round(2)
df2['Mean Drift Depth (m)'] = df2['Mean Drift Depth (m)'].round(2)
df2['Total Drift Area (m<sup>2</sup>)'] = df2['Total Drift Area (m<sup>2</sup>)'].round()
df2['Total Drift Area (m<sup>2</sup>)'] = df2['Total Drift Area (m<sup>2</sup>)'].round(0)
df2['Total Drift Area (m<sup>2</sup>)'] = df2['Total Drift Area (m<sup>2</sup>)'].astype(int)
df2['Total Drift Volume (m<sup>3</sup>)'] = df2['Total Drift Volume (m<sup>3</sup>)'].astype(int)

