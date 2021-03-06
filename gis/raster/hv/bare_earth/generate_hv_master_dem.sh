#!/usr/bin/env bash

echo "Creating Happy Valley Master DEM..."

# 2012 and 2017 DEM Generation Scripts Could Go Here
# But often source data is not kept locally

echo "Subtracting 2012 from 2017 DEM..."

gdal_calc.py -A hv_dem_06_04_2017.tif -B hv_dem_06_07_2012.tif --outfile=hv_2017_2012_dem_difference.tif --calc="A-B" --NoDataValue=-9999

echo "Finding Snowdrifts and filling them with 2012 DEM Values..."
# Ortho sum is computed in a Jupyter notebook, see appendices
gdal_calc.py -A hv_dem_06_07_2012.tif -B orthos/hv_ortho_06_04_2017_sum.tif -C hv_2017_2012_dem_difference.tif --outfile=hv_DemVals2012_where_drifts_in2017Dem_else0.tif --calc="A*(B>420)*(C>0.4)" --overwrite

echo "Computing Mean DEM Values..."

gdal_calc.py -A hv_dem_06_07_2012.tif -B hv_dem_06_04_2017.tif -C hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="((A+B)/2)*(C==0)" --NoDataValue=-9999 --overwrite

echo "Computing DEM Difference with Snowdrifts Masked Out."

gdal_calc.py -A hv_2017_2012_dem_difference.tif -B hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="A*(B>0)" --outfile=hv_2017_2012_dem_difference_outside_of_drifts.tif --NoDataValue=-9999

echo "Adjusting 2017 DEM..."
# A Jupyter Notebook is used to compute the adjustment amount
gdal_calc.py -A hv_dem_06_04_2017.tif --outfile=hv_dem_06_04_2017_adjusted_by_mean_DEM_delta.tif --calc="A-0.13" --overwrite

echo "Filling Masks..."

gdal_calc.py -A hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -B hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif --calc="maximum(A,B)" --NoDataValue=-9999 --overwrite

echo "Padding with 2017 DEM ..."

gdalbuildvrt hv_dem_master.vrt hv_dem_06_04_2017_adjusted_by_mean_DEM_delta.tif hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -vrtnodata -9999 -overwrite

gdalwarp -of Gtiff -dstnodata -9999 hv_dem_master.vrt hv_dem_master.tif -overwrite

echo "Happy Valley Master DEM Complete."

exit 0
