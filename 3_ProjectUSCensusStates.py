# 3_ProjectUSCensusStates.py
# Created on: 2018-04-24
# From Sophie Plassin script
# Description: Project the U.S. states to the projection of the CDL rasters:
#   USA Contiguous Albers Equal Area Conic USGS.
# -----------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
import datetime
from arcpy import env
from arcpy.sa import *


# Set environment settings
dirpath = "C:\\GIS_RGB\\Data\\Administrative_Boundaries\\State\\Raw\\US\\"
arcpy.env.workspace = dirpath

# Set overwrite option
arcpy.env.overwriteOutput = True

# Set local variables
inShape = "tl_2018_us_state.shp" # Unprojected state shapefile
outFeatureSpace = "C:\\GIS_RGB\\Data\\Administrative_Boundaries\\State\\Output\\2018\\" # Save location
fieldState = "STATEFP"
expressionUS = "\"STATEFP\" IN ('08', '35', '48')" # Select Colordao, New Mexico, and Texas
outputSelect = "States_2018.shp" # Save name for unprojected, selected states
outputProj = "States_2018_usa_contiguous_albers.shp" # Save name

#1. SelectLayerByAttribute and write the selected features to a new featureclass

print "Select by attribute starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

arcpy.MakeFeatureLayer_management(inShape, "temp") # Create layer from unprojected US states
arcpy.SelectLayerByAttribute_management("temp", "NEW_SELECTION", expressionUS) # Select CO, NM, TX
outSelect = outFeatureSpace + outputSelect # Path + save name
arcpy.CopyFeatures_management("temp", outSelect) # Save selected states in a new shapefile

print "Select by attribute ends at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")


#2. Project
print "Projection USA contiguous starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

cs = arcpy.SpatialReference("USA Contiguous Albers Equal Area Conic USGS")
projSelect = outFeatureSpace + outputProj # Path + save name
arcpy.Project_management(outSelect, projSelect, cs) # Execute Projection


print "Projection USA contiguous ends at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")


