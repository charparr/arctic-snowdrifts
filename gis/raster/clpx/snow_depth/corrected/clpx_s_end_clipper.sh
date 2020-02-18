#!/usr/bin/env bash

gdalwarp clpx_depth_103_2018_corrected_0.25_m.tif clpx_2018_s_end_depth.tif \
-cutline ../../../../vector/clpx_domain_adjustment/clpx_s_strip_2015_2018_cover.shp -crop_to_cutline 

gdalwarp clpx_depth_102_2017_corrected_0.4_m.tif clpx_2017_s_end_depth.tif \
-cutline ../../../../vector/clpx_domain_adjustment/clpx_s_strip_2015_2018_cover.shp -crop_to_cutline 

gdalwarp clpx_depth_096_2016_corrected_0.38_m.tif clpx_2016_s_end_depth.tif \
-cutline ../../../../vector/clpx_domain_adjustment/clpx_s_strip_2015_2018_cover.shp -crop_to_cutline 

gdalwarp clpx_depth_098_2015_corrected_0.36_m.tif clpx_2015_s_end_depth.tif \
-cutline ../../../../vector/clpx_domain_adjustment/clpx_s_strip_2015_2018_cover.shp -crop_to_cutline 

exit 0
 