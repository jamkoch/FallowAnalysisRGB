# 1_CDL_Preprocessing.py
# Created on: 2019-02-16
# From Sophie Plassin script
# Description: The raw CDL data arrives as a seperate TIFF for each state.
#   Convert these TIFFs to ESRI Grids, remove all background values, mosaic
#   the states, and then mask to the RGB to create one raster per year for
#   the study region.
# ---------------------------------------------------------------------------

# Import arcpy module
import datetime
import arcpy
import os
import glob
import itertools
from arcpy import env
from arcpy.sa import *

print "Geoprocess starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Workspace
env.workspace = "C:\\GIS_RGB\\Geodatabase\\Biophysical\\6_landuse\\US_nass\\original_input\\"
yearList = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

# Extension
arcpy.CheckOutExtension("Spatial")
env.overwriteOutput = True


## 1. CONVERT TIFF TO GRID
# Description:
# We convert the raw raster data (.TIF) to a grid and save the grid in the folder "inter_output" 
#---------------------------

outFolder = "C:\\GIS_RGB\\Geodatabase\\Biophysical\\6_landuse\\US_nass\\inter_output\\"
tifList = arcpy.ListRasters ("*", "TIF")

print "\nStep 1 starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Loop through the list and export tif to grid

for i in range(len(tifList)):
    oName = os.path.splitext(tifList[i])[0]
    outRaster = os.path.join(outFolder, oName)
    arcpy.CopyRaster_management(tifList[i], outRaster, "","","","NONE","NONE","8_BIT_UNSIGNED","NONE","NONE")
    print "Export tif to grid" , tifList[i] , "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 1 Tif to Grid completed at", datetime.datetime.now().strftime("%I:%M:%S%p")
          

## 1.a. Count the number of pixels in Raster Grid

env.workspace = "C:\\GIS_RGB\\Geodatabase\\Biophysical\\6_landuse\\US_nass\\inter_output\\"

gridList = arcpy.ListRasters("*", "GRID")
gridList = sorted(gridList)

def countPixels (listRasters): 
    countList = [] 
    for year in yearList:
        countStateList = []
        pixels = []
        for raster in listRasters:
            # for raster mosaic
            if raster.startswith ("cdl" + year):
                pixels = []
                rows = arcpy.SearchCursor(raster)
                for row in rows:
                    if row.getValue("Value") > 0:
                        pixels.append (row.getValue("Count"))
                        temp = sum(pixels)
                print "NumberPixels_" + year, "=", temp
                countList.append (temp)

            # for list of states
            if raster.startswith("cdl_" + year):
                pixels_state = []
                rows = arcpy.SearchCursor(raster)
                for row in rows:
                    if row.getValue("Value") > 0:
                        pixels_state.append (row.getValue("Count"))
                total_state = sum(pixels_state)
                print str(raster), ": ", total_state
                pixels.append (total_state)
                countStateList.append (raster)
                if len(countStateList) == 3:
                    temp = sum(pixels)
                    print "NumberPixels_" + year, "=", temp
                    countList.append (temp)


    for year, i in itertools.izip(yearList, countList):
        print "year:", year, " NumberPixels:", i
    return countList

print "\nCount the number of pixels in GridList"

countPixels (gridList)


## 2. SET NULL
# Description:
# We run the tool "Set Null" to set to NoData the cells of the grid where VALUE = 0.
# This removes the background of the grid before running the mosaic.
#---------------------------

print "\nStep 2 starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Process Set Null
for i in range(len(gridList)):
    inRaster = gridList[i]
    inFalseRaster = gridList[i]
    whereClause = '"VALUE" = 0'
    outSetNull = SetNull(inRaster, inFalseRaster, whereClause)
    outSetNull.save(gridList[i] + "SN")

    print "Grid to SetNull" , gridList[i] , "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 2 Set Null completed at", datetime.datetime.now().strftime("%I:%M:%S%p")


## 2.a. Count the number of pixels in SetNull
setNullList = arcpy.ListRasters ("*SN", "")
setNullList = sorted(setNullList)
print "\n Count the number of pixels in setNullList"
countPixels (setNullList)

# Check that the number of pixels did not change
def soustraction (listA, listB):  
    for year, a, b in itertools.izip(yearList, countPixels(listA), countPixels(listB)):
        difference = a - b
        if difference == 0:
            print "year:", year, "Same number of pixels"
        if difference != 0:
            print "year:", year, "ERROR: different number of pixels"

print "\nCalculate the difference between gridList and setNullList"

soustraction (gridList, setNullList)


## 3. CREATE A MOSAIC
# Description:
# We run the tool "Mosaic to New Raster" to create a mosaic for each year with the 3 state input rasters (cdl_YY_08sn, cdl_YY_35sn, cdl_YY_48sn).
# All the input rasters have the same projected coordinate system (USA Contiguous Albers Conic)
#---------------------------

coordinate_system = ""
pixel_type="8_BIT_UNSIGNED"
cellsize=""
number_of_bands="1"
mosaic_method="LAST"
mosaic_colormap_mode="FIRST"                  

print "\nStep 3 starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Run Mosaic to New Raster
mosaicList = []
for i in range(len(yearList)):
    newList = [] # empty list for each year
    for raster in setNullList: # loop through all 33 rasters
        if raster.startswith("cdl_" + yearList[i]): # if the same year
            newList.append(raster) # add to newList
            if len(newList) == 3: # once the three state rasters for a given year are added, mosaic them
                print newList
                outRaster = "CDL" + yearList[i] + "_MC"
                arcpy.MosaicToNewRaster_management(newList, outFolder, outRaster, coordinate_system, pixel_type, cellsize, number_of_bands, mosaic_method, mosaic_colormap_mode)
                mosaicList.append(outRaster)
    print "Mosaic" , yearList[i] , "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 3 Mosaic completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

print "\nCount the number of pixels in mosaicList"
countPixels (mosaicList)

# Check that no pixels were lost during the mosaic
print "\nCalculate the difference between setNullList and mosaicList"
soustraction (setNullList, mosaicList)


## 4. PROJECT THE BOUNDARY OF RGB TO USA CONTIGUOUS ALBERS EQUAL AREA CONIC USGS
# Description:
# We run the tool "Project" to project the boundary of the study area to the same projected coordinate system (USA Contiguous Albers Conic) of the raw data.
#---------------------------

folderShapefiles = "C:\\GIS_RGB\\Geodatabase\\rgb_bound\\"
listfc = ["RGB_Basin", "RGB_Ses"]
cs = arcpy.SpatialReference("USA Contiguous Albers Equal Area Conic USGS")
clipList= []

print "\nStep 4 starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

for fc in listfc:
    in_shp = os.path.join(folderShapefiles, fc + ".shp")
    out_shp = os.path.join(folderShapefiles, fc + "_usa_contiguous_albers.shp")
    arcpy.Project_management(in_shp, out_shp, cs)
    clipList.append (out_shp)
    print "Projection" , fc, "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 4 Projection completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

## 5. EXTRACT BY MASK
# Description:
# We run the tool "Extract By Mask" to clip the mosaic to the boundary of the study area
#---------------------------

outFolderFinal = "C:\\GIS_RGB\\Geodatabase\\Biophysical\\6_landuse\\US_nass\\final_output\\"

print "\nStep 5 starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

mosaicList = arcpy.ListRasters ("*MC", "")
print mosaicList

for raster in mosaicList:
    newname = raster.split('_mc')[0]
    newname = os.path.split(newname)[-1]
    newname = newname.lower()
    for clip in clipList:
        temp = os.path.split(clip)[-1]
        if temp.startswith ("RGB_Basin"):
            output = outFolderFinal + newname + "bas"
        else:
            output = outFolderFinal + newname + "ses"
        # Execute ExtractByMask
        outExtractByMask = ExtractByMask(raster, clip)
        # Save the output 
        outExtractByMask.save(output)
        print "Extract By Mask" , str(raster), "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 5 Extract By Mask completed at", datetime.datetime.now().strftime("%I:%M:%S%p")


## 5.a. Count the number of pixels in ClipList
env.workspace = "C:\\GIS_RGB\\Geodatabase\\Biophysical\\6_landuse\\US_nass\\final_output\\"

# Check that each year has the same number of pixels

sesList = arcpy.ListRasters("*ses", "GRID")
print sesList
sesList = sorted(sesList)
print "\nCount the number of pixels in Ses List"
countPixels (sesList)

basinList = arcpy.ListRasters("*bas", "GRID")
basinList = sorted(basinList)
print "\nCount the number of pixels in Basin List"
countPixels (basinList)

