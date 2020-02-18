#!/usr/bin/env python
# coding: utf-8

import rasterio
import rasterio.mask
import fiona
import numpy as np

src = rasterio.open('hv_dem_master.tif')
dem = src.read(1)
profile = src.profile

with fiona.open('../../vector/hv_lake.shp', "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

lake_masks = {}

i=1
for lake in shapes:
    lake_masks[i] = {}
    lake_masks[i]['msk'], lake_masks[i]['t'] = rasterio.mask.mask(src, [lake], nodata=-9999.0)
    lake_masks[i]['msk'][lake_masks[i]['msk'] < 0] = np.nan
    lake_masks[i]['msk'] = lake_masks[i]['msk'][0]
    lake_masks[i]['msk_nanmean'] = np.nanmean(lake_masks[i]['msk'])
    i += 1
lake_masks

new_dem = np.copy(dem)

for l_mask in lake_masks:
    
    new_dem[np.where(~np.isnan(lake_masks[l_mask]['msk']))] = lake_masks[l_mask]['msk_nanmean']

new_dem[new_dem == new_dem.max()] = profile['nodata']

output = 'hv_dem_flattened_lakes.tif'
with rasterio.open(output, 'w', **profile) as dst:
    dst.write(new_dem, 1)





