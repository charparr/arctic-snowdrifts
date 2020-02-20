#!/usr/bin/env bash

gdalwarp ../../hv_depth_103_2018_corrected_-0.08_m.tif hv_snow_depth_ice_wedge_2018.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline 

gdalwarp ../../hv_depth_102_2017_corrected_-0.05_m.tif hv_snow_depth_ice_wedge_2017.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline 

gdalwarp ../../hv_depth_096_2016_corrected_0.00_m.tif hv_snow_depth_ice_wedge_2016.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline 

gdalwarp ../../hv_depth_098_2015_corrected_0.18_m.tif hv_snow_depth_ice_wedge_2015.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline 

gdalwarp ../../hv_depth_103_2013_corrected_-0.03_m.tif hv_snow_depth_ice_wedge_2013.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline 

gdalwarp ../../hv_depth_107_2012_corrected_-0.04_m.tif hv_snow_depth_ice_wedge_2012.tif \
-cutline ../../../../../../vector/subset_polygons/hv_ice_wedge_clipper.shp -crop_to_cutline

exit 0
