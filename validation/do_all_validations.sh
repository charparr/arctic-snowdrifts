#!/usr/bin/env bash

echo "Validating CLPX Snow Depth Maps..."

echo "2018..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2018/magnaprobe_validation_points/clpx_all_depths_2018_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_103_2018.tif -out_results=True -outrstr=True &&

echo "2017..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2017/magnaprobe_validation_points/clpx_all_depths_2017_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_102_2017.tif -out_results=True -outrstr=True &&

echo "2016..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2016/magnaprobe_validation_points/clpx_all_depths_2016_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_096_2016.tif  -out_results=True -outrstr=True &&

echo "2015..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2015/magnaprobe_validation_points/clpx_all_depths_2015_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_098_2015.tif -out_results=True -outrstr=True &&

echo "2013..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2013/magnaprobe_validation_points/clpx_all_depths_2013_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_103_2013.tif -out_results=True -outrstr=True &&

echo "2012..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/clpx/2012/magnaprobe_validation_points/clpx_all_depths_2012_utm.shp \
-dDEM ../gis/raster/clpx/snow_depth/uncorrected/clpx_depth_107_2012.tif -out_results=True -outrstr=True &&

echo "Validating Happy Valley Snow Depth Maps..."

echo "2018..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/hv/2018/magnaprobe_validation_points/hv_all_depths_2018_utm.shp \
-dDEM ../gis/raster/hv/snow_depth/uncorrected/hv_depth_103_2018.tif -out_results=True -outrstr=True &&

echo "2017..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/hv/2017/magnaprobe_validation_points/hv_all_depths_2017_utm.shp \
-dDEM ../gis/raster/hv/snow_depth/uncorrected/hv_depth_102_2017.tif -out_results=True -outrstr=True &&

echo "Note: No MagnaProbe Validation Data for Happy Valley 2016"

echo "2015..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/hv/2015/magnaprobe_validation_points/hv_all_depths_2015_utm.shp \
-dDEM ../gis/raster/hv/snow_depth/uncorrected/hv_depth_098_2015.tif -out_results=True -outrstr=True &&

echo "2013..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/hv/2013/magnaprobe_validation_points/hv_all_depths_2013_utm.shp \
-dDEM ../gis/raster/hv/snow_depth/uncorrected/hv_depth_103_2013.tif -out_results=True -outrstr=True &&

echo "2012..."
python compute_validation_no_plots.py -shp ../gis/vector/magnaprobes/hv/2012/magnaprobe_validation_points/hv_all_depths_2012_utm.shp \
-dDEM ../gis/raster/hv/snow_depth/uncorrected/hv_depth_107_2012.tif -out_results=True -outrstr=True &&

echo "Validation Complete for All Snow Depth Maps."

# python aggregate_validation_stats.py &&

# echo "Validation Results Summarized and Aggregated."

# python error_v_easting_northing.py &&

# python error_v_slope_aspect.py -shp ../

# echo "Terrain vs. Error Analysis Complete."

echo "validation Completed."

exit 0
