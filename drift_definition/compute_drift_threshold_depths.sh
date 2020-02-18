#!/usr/bin/env bash

echo "Computing Annual and Mean Annual Happy Valley Drift Thresholds ..."

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_107_2012_corrected_-0.04_m.tif

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_103_2013_corrected_-0.03_m.tif

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_098_2015_corrected_0.18_m.tif

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_096_2016_corrected_0.00_m.tif

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_102_2017_corrected_-0.05_m.tif

python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_103_2018_corrected_-0.08_m.tif

# python drift_definer.py -d ../gis/raster/hv/snow_depth/corrected/hv_depth_stack_mean.tif

echo "Computing Annual and Mean Annual CLPX Drift Thresholds ..."

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_107_2012_corrected_0.16_m.tif

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_103_2013_corrected_0.21_m.tif

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_098_2015_corrected_0.36_m.tif

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_096_2016_corrected_0.38_m.tif

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_102_2017_corrected_0.4_m.tif

python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_103_2018_corrected_0.25_m.tif

# python drift_definer.py -d ../gis/raster/clpx/snow_depth/corrected/clpx_depth_stack_mean.tif

echo "Drift Threshold Computation Complete."

exit 0
