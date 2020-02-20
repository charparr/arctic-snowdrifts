#!/usr/bin/env bash

gdalwarp ../../clpx_depth_103_2018_corrected_0.25_m.tif clpx_snow_depth_watertracks_creek_2018.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline 

gdalwarp ../../clpx_depth_102_2017_corrected_0.4_m.tif clpx_snow_depth_watertracks_creek_2017.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline 

gdalwarp ../../clpx_depth_096_2016_corrected_0.38_m.tif clpx_snow_depth_watertracks_creek_2016.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline 

gdalwarp ../../clpx_depth_098_2015_corrected_0.36_m.tif clpx_snow_depth_watertracks_creek_2015.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline 

gdalwarp ../../clpx_depth_103_2013_corrected_0.21_m.tif clpx_snow_depth_watertracks_creek_2013.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline 

gdalwarp ../../clpx_depth_107_2012_corrected_0.16_m.tif clpx_snow_depth_watertracks_creek_2012.tif \
-cutline ../../../../../../vector/subset_polygons/clpx_watertracks_creek_clipper.shp -crop_to_cutline

exit 0
