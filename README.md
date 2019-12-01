# FallowAnalysisRGB

This repository contains all of the scripts used to process and analyze the spatio-temporal patterns of fallow in the U.S. portion of the Rio Grande Socio-Environmental System (SES).

Data processing:
*1_CDL_Preprocessing.py
*2_ProjectEcoregions.py
*3_ProjectUSCensusStates.py
*4_CDL_FallowGeoprocessing.py

*1_CDL_Preprocessing.py generates gridded annual maps of land-use from the U.S. Department of Agriculture's Cropland Data Layer (CDL).
The output dataset (rasters) has the extent of the Rio Grande SES at a 30 m resolution for the 11-year period of 2008-2018.
The input dataset – CDL annual time series for the states of Colorado, New Mexico and Texas - are downloadable as raster-based GeoTIFF files from the web application CropScape: https://nassgeodata.gmu.edu/CropScape/. 
The boundary of the study area (Rio Grande SES) is downloadable at https://doi.org/10.17605/OSF.IO/79426

*2_ProjectEcoregions.py projects the U.S. Level 3 Ecoregions polygon shapefile to the same projection of the CDL rasters: USA Contiguous Albers Equal Area Conic USGS.
The input dataset – Level III Ecoregions of North America Shapefile – is downloadable at https://www.epa.gov/eco-research/ecoregions-north-america

*3_ProjectUSCensusStates.py projects the U.S. states to the projection of the CDL rasters: USA Contiguous Albers Equal Area Conic USGS.
The input dataset – 2018 TIGER/Line® Shapefiles States (and equivalent) for the entire U.S. – is downloadable at https://www.census.gov/cgi-bin/geo/shapefiles/index.php

*4_CDL_FallowGeoprocessing.py generates a time-series that reports the sequences of land-use for all pixels contained within the mask of the maximum agricultural areal extent (areas that has been at least one time cropland or fallow land during the 11-year period of 2008-2018).
The script runs with three input dataset – the CDL gridded annual maps for the 11-year period of 2008-2018, the ecoregions and states boundaries – which are derived from steps 1, 2 and 3.

