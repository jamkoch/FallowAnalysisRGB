# 4_CDL_FallowGeoprocessing.py
# Created on: 2019-04-26
# From Madison Wilson, Kevin Neal, Sophie Plassin
# Description: Quantifying fallow/idle and cropland spatial extent and frequencies
#       from 2008 - 2018 using the USDA NASS's Cropland Data Layer.
# --------------------------------------------------------------------------------

import datetime
import arcpy
import os
from arcpy import env
from arcpy.sa import *

print "Geospatial data process starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Set environment
env.workspace = "H:/CDL_RGB/usa_albers"
env.overwriteOutput = True

# Check out extensions
arcpy.CheckOutExtension ("Spatial")

## HOW TO RUN THIS CODE ##
# 1. Run steps 1,2,3,4 in ESRI'S ArcGIS Python Window
# 2. Comment out steps 2,3,4 (NOT step 1)
# 3. Run the code in IDLE
#------------------------

## 1. Import CDL Rasters for Whole RGB for 2008 - 2018
# Never comment out Step 1

unsortedStringPath = []
sortedStringPath = []
raster = []

# H:/CDL_RGB/usa_albers/output_data/mosaic_ses contains the 11 CDL RGB rasters
# Import the file names of the 11 CDL RGB rasters
for file in os.listdir("H:/CDL_RGB/usa_albers/output_data/mosaic_ses"):
    if file.endswith("ses"):
        temp = file
        unsortedStringPath.append(temp)

# Sort the file names alphabetically
sortedStringPath = sorted(unsortedStringPath)
print sortedStringPath

# Turn the list of path names into a list of raster files
for year in sortedStringPath:
    tempRaster = Raster("H:/CDL_RGB/usa_albers/output_data/mosaic_ses/" + year)
    raster.append(tempRaster)

# Create a list of years to be used later for naming files.
folderlist = ["08" , "09" , "10" , "11" , "12" ,
              "13" , "14" , "15" , "16" , "17", "18"]

#------------------------

## Steps 2, 3, and 4 need to be run in ArcMaps's Python Window.

#### 2. CROPLAND RECLASSIFY
## [2008 - 2018 Cropland] ##
# Inputs:  rasters: The 11 CDL RGB rasters.
# Outputs: cropReclassList: One binary raster per year with (crops or fallow/idle = 1) and (non-crop = 0).

print '\nStep 2 Reclassify Cropland started at', datetime.datetime.now().strftime("%I:%M:%S%p")

# Reclasify the yearly rasters of the whole RGB so crops or fallow = 1 and non-crop = 0
cropReclassList = []
for i in range(len(raster)):
    savename = "H:/CDL_RGB/usa_albers/output_data/crop/rcCropCDL/croprc" + folderlist[i]
    inRaster = raster[i]
    # 61 = fallow/idle
    cropRemapRange = RemapRange([[1, 61, 1], [61, 65, 0], [65, 77, 1], [80, 195, 0], [203, 254, 1]])
    outCropRC = Reclassify(inRaster, "VALUE", cropRemapRange) # Reclassify
    cropReclassList.append(savename) # Append path name to a list
    outCropRC.save(savename) # Save
    print "cropRC",folderlist[i], "completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Turn the list of path names into a list of raster files.
for i in range(len(cropReclassList)):
    cropReclassList[i] = Raster(cropReclassList[i])
    
print 'Step 2 Reclassify Cropland completed at', datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 3. CROPLAND CONDITIONAL
##
# Inputs:  cropReclassList
# Outputs: cropland: A raster containing the maximum extent of agricultural land (crops or fallow/idle)

print '\nStep 3 Cropland Conditional started at', datetime.datetime.now().strftime("%I:%M:%S%p")
# Agricultural land is all land that was cropland or fallow/idle for any year in the time series
# Create one raster where 1 = agricultural land in any year and 0 = never agricultural land
CropCon = (Con(((cropReclassList[0] == 1) | (cropReclassList[1] == 1) | (cropReclassList[2] == 1) | (cropReclassList[3] == 1) |
                (cropReclassList[4] == 1) | (cropReclassList[5] == 1) | (cropReclassList[6] == 1) | (cropReclassList[7] == 1) |
                (cropReclassList[8] == 1) | (cropReclassList[9] == 1) | (cropReclassList[10] == 1)) , 1 , 0))
conSave = "H:/CDL_RGB/usa_albers/output_data/crop/cropland" # Path + name
CropCon.save(conSave) # Save

print "Step 3 Cropland Conditional completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 4. CELL STATISTICS SUM CROPLAND FREQUENCY
##
# Inputs:  cropReclassList
# Outputs: cropfreq: a raster with the number of years that a pixel was agricultural land

print '\nStep 4 Cell Statistics Sum Cropland Frequency started at', datetime.datetime.now().strftime("%I:%M:%S%p")

# Create crop + fallow frequency raster
cropfreqsave = "H:/CDL_RGB/usa_albers/output_data/frequency/cropfreq"
cropFreqCS = CellStatistics(cropReclassList, "SUM", "NODATA") # Sum the reclassified binary rasters
cropFreqCS.save(cropfreqsave) # Save

print "Step 4 Cell Statistics Sum Cropland Frequency completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 5. CROPLAND NoData RECLASSIFY 
## 
# Inputs:  cropland
# Outputs: reclassCrop: cropland raster with zeros changed to "NO DATA"

print "\nStep 5 Cropland NoData Reclassify starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

inRaster = "H:/CDL_RGB/usa_albers/output_data/crop/cropland"
reclassField = "VALUE"
remap = RemapValue([[0 , "NODATA"] ,
                    [1 , 1]])

# Reclassify the zeros in the cropland raster to No Data
outReclassify = Reclassify(inRaster ,
                           reclassField ,
                           remap)
outReclassify.save("H:/CDL_RGB/usa_albers/output_data/crop/reclassCrop") # Save

print "Step 5 Cropland NoData Reclassify completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 6. CREATE A GEODATABASE
## The arcpy.AlterField_management function (in Step 8) will only work in a geodatabase.
#

print "\nStep 6 Create a geodatabase starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

out_folder_path = "H:/CDL_RGB/usa_albers/output_data"
out_name = "Crops.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path ,
                               out_name)

print "Step 6 Create a geodatabase created at" , datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 7. RASTER TO POINTS
##
# Inputs:  reclassCrop
# Outputs: rcCrop: reclassCrop, but converted to points

print "\nStep 7 Convert Raster to Points starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Convert the reclassified cropland raster to points
RasterReclass = "H:/CDL_RGB/usa_albers/output_data/crop/reclassCrop"
outPoint = "H:/CDL_RGB/usa_albers/output_data/Crops.gdb/rcCrop" # Save in the geodatabase
field = "VALUE"
arcpy.RasterToPoint_conversion(RasterReclass ,
                               outPoint ,
                               field)

print "Step 7 reclassCrop to points (rcCrop) completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 8. EXTRACT VALUES TO POINTS
##
# Inputs:  rcCrop
# Outputs: ExCrop2018: rcCrop with additional columns in the attribute table containing the CDL values for each year

print "\nStep 8 Extract Values to Points starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Using the reclassifed point file, add fields containing the CDL values at each point for 2008 - 2018

inPointFeatures = []
inPointFeatures.append("/output_data/Crops.gdb/rcCrop") # maximum agricultural extent point file

gdb = "/output_data/Crops.gdb/"

fieldAlter = "RASTERVALU" # The field name we want to change
yearList = ["2008" , "2009" , "2010" , "2011" , "2012" ,
            "2013" , "2014" , "2015" , "2016" , "2017", "2018"]

for i in range(len(yearList)):
    inPointFeat = inPointFeatures[-1] # Use the most recent file appended to inPointFeatures
    outPointFeature = gdb + "ExCrop" + yearList[i] # save name based on the year

    # Extract the values from the RGB CDL rasters to the cropland point file
    ExtractValuesToPoints(inPointFeat ,
                          raster[i] ,
                          outPointFeature ,
                          "NONE" ,
                          "VALUE_ONLY")

    print inPointFeat
    print "Extract Values to Points for" , yearList[i] , "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

    # Change the field name to match the year
    arcpy.AlterField_management(outPointFeature ,
                                fieldAlter ,
                                "CDL_" + yearList[i] ,
                                "CDL_" + yearList[i])
    # Append the file containing the new field name to inPointFeatures
    inPointFeatures.append(outPointFeature)

    print "AlterFieldManagement for" , yearList[i] , "completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")

print "Step 8 Extract Values to Points completed at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

#------------------------

#### 8.1 ADD STATE AND ECOREGION CODES
##
# Inputs:  ExCrop2018, ecoregions shapefile, states shapefile, RGB boundary shapefile
# Outputs: ExCrop2018 with additional fields identifying the Level 3 Ecoregion and state each point lies in

# 8.1.1. CREATE A GEODATABASE

print "\nStep 8.1.1 Create a geodatabase starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Create a new geodatabase that only will only contain the final output point file
out_folder_path = "H:/CDL_RGB/usa_albers/output_data"
out_name = "Crops2018.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path,
                               out_name)

print "Geodatabase created at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

new_gdb = os.path.join(out_folder_path, out_name)
in_fc = "H:/CDL_RGB/usa_albers/output_data/Crops.gdb/ExCrop2018" # cropland point file
out_fc = new_gdb + "/ExCrop2018"

print "Copy feature to new gdb", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

arcpy.CopyFeatures_management(in_fc, out_fc) # Copy the cropland point file into the new gdb

print "Copy feature to new gdb completed at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

print "Delete grid_code", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

arcpy.DeleteField_management (out_fc, "grid_code") # Delete the grid_code field

print "Delete grid_code completed at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")


ecoShape =   "H:/CDL_RGB/usa_albers/output_data/ecoregions/na_eco_3_usa_contiguous_albers.shp" # polygons: U.S. Level 3 Ecoregions
stateShape = "H:/CDL_RGB/usa_albers/output_data/states/States_2018_usa_contiguous_albers.shp" # polygons: U.S. States
cropFile =   "H:/CDL_RGB/usa_albers/output_data/Crops2018.gdb/ExCrop2018" # point file in the new gdb
rgbShape =   "H:/CDL_RGB/usa_albers/output_data/rgb_bound/RGB_Ses_usa_contiguous_albers.shp" # polygon: shape of RGB

print "\nStep 8.1 Add codes for ecoregions and states starts at", datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")

# Add empty state and ecoregion columns to the point file
arcpy.AddField_management(cropFile, "state_code", "TEXT", "", "", "2")
arcpy.AddField_management(cropFile, "eco3_code", "TEXT", "", "", "10")
print "Add new fields completed at" , datetime.datetime.now().strftime("%I:%M:%S%p")


# Create layers
arcpy.MakeFeatureLayer_management(ecoShape, "lyr_ecoregion")
arcpy.MakeFeatureLayer_management(stateShape, "lyr_state")
arcpy.MakeFeatureLayer_management(cropFile, "point_lyr")
arcpy.MakeFeatureLayer_management(rgbShape, "lyr_rgb")

print "Temporary feature layers completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Select by location the ecoregions in the RGB
arcpy.SelectLayerByLocation_management("lyr_ecoregion",
                                       "INTERSECT",
                                       "lyr_rgb",
                                       "",
                                       "NEW_SELECTION")

print "Selected all ecoregions intersecting the RGB", datetime.datetime.now().strftime("%I:%M:%S%p")

# Copy ecoregions and states code in fields
lyrList = ["lyr_state", "lyr_ecoregion"]

# For any point not in an ecoregion or state, fill the CODE field with 99
for i in range(len(lyrList)):
    # Select all points intersecting the layer, then invert the selection
    arcpy.SelectLayerByLocation_management("point_lyr",
                                           "INTERSECT",
                                           lyrList[i],
                                           "", "NEW_SELECTION", "INVERT")
    # Select the correct code column to fill in based on which layer (eco or state) is being use      
    if lyrList[i] == "lyr_ecoregion" :
        field_lyr = "eco3_code"
    else:
        field_lyr = "state_code"
    # Fill in the column with 99
    arcpy.CalculateField_management("point_lyr",
                                    field_lyr,
                                    "'{0}'".format(str("99")),
                                    "PYTHON_9.3", "")
print "Added 99 values", datetime.datetime.now().strftime("%I:%M:%S%p")

# Add the codes for the ecoregion and state each point intersects to the point file attribute table
for i in range(len(lyrList)):
    cur = arcpy.UpdateCursor(lyrList[i])
    for row in cur:
        # Select individual ecoregions and states one polygon at a time
        arcpy.SelectLayerByAttribute_management(lyrList[i],
                                                "NEW_SELECTION",
                                                "\"FID\" = " + str(row.getValue("FID")))
        # Then select all the points in that ecoregion or state
        arcpy.SelectLayerByLocation_management("point_lyr",
                                               "INTERSECT",
                                               lyrList[i],
                                               "", "NEW_SELECTION")
        # Choose code column based on the layer     
        if lyrList[i] == "lyr_ecoregion":
            field_lyr = "eco3_code"
            field_original = "NA_L3CODE"
        if lyrList[i] == "lyr_state":
            field_lyr = "state_code"
            field_original = "STATEFP"
        # And fill the CODE field
        arcpy.CalculateField_management("point_lyr",
                                        field_lyr,
                                        "'{0}'".format(str(row.getValue(field_original))),
                                        "PYTHON_9.3", "")
    print "Add code", lyrList[i], "completed at" , datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")


print "Step 8.1 Add codes for ecoregions and states completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 8.2 EXPORT FALLOW CROPLAND
##
# Inputs:  ExCrop2018
# Outputs: fallowcrops .csv & .shp: point file & csv containing the maximum extent of fallow/idle cropland

## Select By Attributes all points that were ever fallow and export to a new shapefile

print "\nStep 8.2 Export Fallow Cropland starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Create layer from the point file ExCrop2018
arcpy.MakeFeatureLayer_management(cropFile, "point_lyr")

# Select all points that were fallow (61) in the time series
fallowQuery = "CDL_2008 = 61 OR CDL_2009 = 61 OR CDL_2010 = 61 OR CDL_2011 = 61 OR CDL_2012 = 61 OR CDL_2013 = 61 OR CDL_2014 = 61 OR CDL_2015 = 61 OR CDL_2016 = 61 OR CDL_2017 = 61 OR CDL_2018 = 61"
arcpy.SelectLayerByAttribute_management("point_lyr", "NEW_SELECTION", fallowQuery)

# Copy selection to a new shapefile
fallowcrops = "H:\\CDL_RGB\\usa_albers\\output_data\\fallow_cropland\\fallowcrops.shp"
arcpy.CopyFeatures_management("point_lyr", fallowcrops)

print "Copy Features: Fallow Cropland completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

print "Fallow Cropland export to ASCII starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Export the attribute table to CSV
Output_ASCII_file = "H:\\CDL_RGB\\usa_albers\\output_data\\fallow_cropland\\csvs\\fallowcrops.csv"
arcpy.ExportXYv_stats(fallowcrops,
                      "pointid;CDL_2008;CDL_2009;CDL_2010;CDL_2011;CDL_2012;CDL_2013;CDL_2014;CDL_2015;CDL_2016;CDL_2017;CDL_2018;eco3_code;state_code",
                      "COMMA",
                      Output_ASCII_file,
                      "ADD_FIELD_NAMES")

print "Step 8.2 Export Fallow Cropland completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 8.3 EXPORT FALLOW CROPLAND, AND CROPLAND BASED ON ECOREGION AND STATE
##
# Inputs:  ExCrop2018
# Outputs: one shapefile and one csv for each ecoregion and state (to include the 99 values) for both fallow/idle and cropland

print "\nStep 8.3. Export to csv Based on Ecoregion and State starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

## Create several common variables and functions:
ecofield = 'eco3_code'
statefield = 'state_code'
fieldList = [ecofield, statefield]
nameList = ["eco", "state"]

# Create a function that creates sets of the unique values in a field
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

# Create a function that converts the sets to lists of strings
def convert(List):
    for i in range(len(List)):
        for j in range(len(List[i])):
            List[i][j] = str(List[i][j])
    return List

# Create a function that removes the periods from the unique ecoregion codes
def eco_values(ecoValues):
    newEcoValues = []
    for i in range(len(ecoValues)):
        if ecoValues[i] == "99":
            ecoCode = "99"
        else:    
            firstpoint = ecoValues[i].find(".")
            middle = firstpoint + 1
            secondpoint = ecoValues[i].find(".", middle)
            ecoCode = ecoValues[i][:firstpoint] + ecoValues[i][middle] + ecoValues[i][secondpoint + 1:]
        newEcoValues.append(ecoCode)
    return newEcoValues

# Create a function that creates new shapefiles and csvs for each ecoregion/state
def export (List, layer, folder_shp, folder_csv):
    for i in range(len(List)): # Loop through the ecoregions, then the states
        # Loop through the unique values
        for j in range(len(List[i])):
            # Select all points in the specifed ecoregion or state        
            query = fieldList[i] + " = '" + List[i][j] + "'"
            print "Select Layer By Attribute for", layer + "_" + nameList[i] + nameCodes[i][j], "starts at", datetime.datetime.now().strftime("%I:%M:%S%p")
            arcpy.SelectLayerByAttribute_management(layer, 
                                                    "NEW_SELECTION", 
                                                    query)
            
            # Copy the selection into a new shapefile
            print "Copy Features for", layer + "_" + nameList[i] + nameCodes[i][j], "starts at", datetime.datetime.now().strftime("%I:%M:%S%p")
            savename = folder_shp + layer + "_" + nameList[i] + nameCodes[i][j] + ".shp"
            arcpy.CopyFeatures_management(layer, savename)
            
            # Export the new shapefile to a csv
            print "ASCII export for", layer + "_" + nameList[i] + nameCodes[i][j], "starts at", datetime.datetime.now().strftime("%I:%M:%S%p")
            Output_ASCII_file = folder_csv + layer + "_" + nameList[i] + nameCodes[i][j] + ".csv"
            arcpy.ExportXYv_stats(savename,
                                  "pointid;CDL_2008;CDL_2009;CDL_2010;CDL_2011;CDL_2012;CDL_2013;CDL_2014;CDL_2015;CDL_2016;CDL_2017;CDL_2018;eco3_code;state_code",
                                  "COMMA",
                                  Output_ASCII_file,
                                  "ADD_FIELD_NAMES")


# 8.3.1. Export fallow cropland based on Ecoregion and State
print "\nStep 8.3.1 Export Fallow Cropland Based on Ecoregion and State starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

arcpy.MakeFeatureLayer_management(fallowcrops, "fallowcrop") # create layer from fallowcrops (point file of max extent of fallow)

ecoValues_F = unique_values(fallowcrops, ecofield) # Unique Ecoregion values
stateValues_F = unique_values(fallowcrops, statefield) # Unique State values
valueList_F = [ecoValues_F, stateValues_F]

convert(valueList_F) # Convert the sets to lists of strings

newEcoValues_F = eco_values(ecoValues_F) # Create a list of the Ecoregion Values without the periods

nameCodes = [newEcoValues_F, stateValues_F] # Create lists to be used when naming state and ecoregion files

# Create new shapefiles and csvs for each ecoregion/state and 99 values
export(valueList_F,
       "fallowcrop",
       "H:\\CDL_RGB\\usa_albers\\output_data\\fallow_cropland\\ecoregion_state_outputs\\",
       "H:\\CDL_RGB\\usa_albers\\output_data\\fallow_cropland\\csvs\\")

print "Step 8.3.1 Export Fallow Cropland Based on Ecoregion and State completed at", datetime.datetime.now().strftime("%I:%M:%S%p")


# 8.3.2. Export cropland Based on Ecoregion and State
print "\nStep 8.3.2 Export Cropland Based on Ecoregion and State starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

arcpy.MakeFeatureLayer_management(cropFile, "crop") # Create layer from crop (point file of max extent of crops)

ecoValues_C = unique_values(cropFile, ecofield) # Unique Ecoregion values
stateValues_C = unique_values(cropFile, statefield) # Unique State Values
valueList_C = [ecoValues_C, stateValues_C]

convert(valueList_C) # Convert the sets to lists of stings

newEcoValues_C = eco_values(ecoValues_C) # Create a list of the Ecoregion Values without the periods

nameCodes = [newEcoValues_C, stateValues_C] # Create lists to be used when naming state and ecoregion files

# Create new shapefiles and csvs for each ecoregion/state and 99 values
export(valueList_C,
       "crop",
       "H:\\CDL_RGB\\usa_albers\\output_data\\crop\\ecoregion_state_outputs\\",
       "H:\\CDL_RGB\\usa_albers\\output_data\\crop\\csvs\\")

print "Step 8.3.2 Export Cropland Based on Ecoregion and State completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 9. EXPORT FEATURE ATTRIBUTE TO ASCII
##
# Inputs:  ExCtop2018
# Outputs: cropland.csv: a CSV file containing the attribute table from ExCrop2018.shp

print "\nStep 9 Beginning Feature Attribute to ASCII", datetime.datetime.now().strftime("%I:%M:%S%p")

Input_Feature_Class = ("H:/CDL_RGB/usa_albers/output_data/Crops2018.gdb/ExCrop2018") # The input final point file
Output_ASCII_file = ("H:/CDL_RGB/usa_albers/output_data/crop/csvs/cropland.csv") # Path and save name of CSV output

# Export to CSV:
arcpy.ExportXYv_stats(Input_Feature_Class,
                      "pointid;CDL_2008;CDL_2009;CDL_2010;CDL_2011;CDL_2012;CDL_2013;CDL_2014;CDL_2015;CDL_2016;CDL_2017;CDL_2018;eco3_code;state_code",
                      "COMMA",
                      Output_ASCII_file,
                      "ADD_FIELD_NAMES")

print "Step 9 Export Feature Attribute to ASCII complete at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 10. CREATE FALLOW CROPLAND FREQUENCY RASTER
##
# Inputs: Original 11 CDL rasters
# Outputs: reclassify##: 11 binary rasters representing the yearly max extent of fallow/idle
#          fallowFreq: a raster with the number of years that a pixel was fallow/idle

print "\nStep 10 Create Fallow Cropland Frequency Raster starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Reclassify the CDL rasters for the Whole RGB so 61 = 1 and Not 61 = 0

## For land use that are fallow/idle (61):
## If Value = 61, NewValue = 1
##
## For all land use that are not fallow/idle:
## If range between 1 and 60, NewValue = 0
## If range between 62 and 248 (to include 247), NewValue = 0

fallowreclasslist = [] # Empty loop to store reclassified binary fallow rasters
for i in range(len(raster)): # Loop through the original CDL RGB rasters
    savename = "H:/CDL_RGB/usa_albers/output_data/fallow_cropland/rcFallowCDL/reclassify" + folderlist[i] # save name based on year
    inRaster = raster[i] # Yearly CDL RGB raster
    myRemapRange = RemapRange([[1, 60, 0], [61, 1], [61, 247, 0]]) # Reclassify fallow/idle (61) to 1, else to 0
    outReclassRR = Reclassify(inRaster, "VALUE", myRemapRange) # Execute Reclassify
    outReclassRR.save(savename) # Save new binary raster
    fallowreclasslist.append(savename) # Append path + save name to a list
    print "fallowRC",folderlist[i], "completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

## Add the Reclassified rasters to create a frequency raster of fallow cropland
print "Cell Statistics Sum Fallow Cropland Frequency starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

output_location = "H:/CDL_RGB/usa_albers/output_data/frequency/fallowFreq" # Path and save name of fallow frequency raster
fallowFreqRas = CellStatistics(fallowreclasslist, "SUM", "NODATA") # Execute CellStatistics (sum individual pixels)
fallowFreqRas.save(output_location) # Save

print "Step 10 Fallow Cropland Frequency Raster completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

#### 11. CREATE CROP ONLY FREQUENCY RASTER
##
# Inputs:  cropfreq and fallowfreq
# Outputs: croponly: a raster with the number of years that a pixel was cropland (excluding fallow/idle)

print "\nStep 11 Crop Only Frequency Raster starts at", datetime.datetime.now().strftime("%I:%M:%S%p")

# Subtract fallow frequency from the agricultural land frequency
raster1 = Raster("H:/CDL_RGB/usa_albers/output_data/frequency/cropfreq")
raster2 = Raster("H:/CDL_RGB/usa_albers/output_data/frequency/fallowfreq")
crop_freq = raster1 - raster2 # agricultural land frequency - fallow/idle frequency = cropland frequency
crop_freq.save("H:/CDL_RGB/usa_albers/output_data/frequency/croponly") # Save

print "Step 11 Crop Only Frequency Raster completed at", datetime.datetime.now().strftime("%I:%M:%S%p")

#------------------------

print "\nProgram complete." , datetime.datetime.now().strftime("%A, %B %d %Y %I:%M:%S%p")
