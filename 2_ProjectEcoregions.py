# 2_ProjectEcoregions.py
# Created on: 2018-04-24
# From Sophie Plassin script
# Description: Project the U.S. Level 3 Ecoregions polygon shapefile to the
#   projection of the CDL rasters: USA Contiguous Albers Equal Area Conic USGS.
# -----------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
import datetime
from arcpy import env
from arcpy.sa import *


# Set environment settings
dirpath = "C:\\GIS_RGB\\Data\\Ecoregion\\Raw\\EPA\\"
arcpy.env.workspace = dirpath
outFeatureSpace = "C:\\GIS_RGB\\Data\\Ecoregion\\Output\\EPA\\"

# Set overwrite option
arcpy.env.overwriteOutput = True

# Set local variables
inShapeList = arcpy.ListFeatureClasses()
cs = arcpy.SpatialReference("USA Contiguous Albers Equal Area Conic USGS")

#1. Project
print "Projection USA contiguous starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

for shp in inShapeList:
    print shp
    if shp.startswith ("NA_CEC"):
        outProj = "na_eco_3_usa_contiguous_albers.shp"
    else:
        outProj = "us_eco_4_usa_contiguous_albers.shp"
    arcpy.Project_management(shp, outFeatureSpace + outProj, cs)

print "Projection USA contiguous ends at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")


