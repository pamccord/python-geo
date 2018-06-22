#This script was produced to process all geospatial data for the
#Agricultural Intensification paper based on the Kastens et al (2017) data.
#Author: Paul McCord, Date Created: 3-30-18

#import modules
import arcpy
from arcpy.sa import *
import os
import string

arcpy.env.overwriteOutput = True
arcpy.env.snapRaster = "D:\\AgIntensificationData\\Kastens_landCover\\MT_land_cover_CY2001.img"
arcpy.env.cellSize = "D:\\AgIntensificationData\\Kastens_landCover\\MT_land_cover_CY2001.img"
arcpy.CheckOutExtension("Spatial")

"""
###
#The AvgOctToMar NDVI data had two years come in separate downloads. These separate files are mosaicked together

#The mosaic function
def mosaic(mosaicSets):
	print mosaicSets
	print "mosaicSets: " + mosaicSets[0] + " and " + mosaicSets[1]
	mosaicSets2 = ','.join(mosaicSets)
	mosaicSets3 = mosaicSets2.replace(",", ";")
	mosaicSets3 = '"' + mosaicSets3 + '"'
	outputLocation = ws
	outName = str(mosaicSets[0][:2]) + "rsAvg.tif"
	print "mosaicking " + mosaicSets3 + " together."
	arcpy.MosaicToNewRaster_management(mosaicSets3, outputLocation, outName, "4326", "64_BIT", "0.00224579", "1", "LAST", "FIRST")

#Preparing data for the mosaic function
ws = "D:\\AgIntensificationData\\ndvi\\AvgOctToMar\\"
arcpy.env.workspace = ws
mosaicList = []
rasters = arcpy.ListRasters()
for r in rasters:
	if r[-6:] == '_1.tif' or r[-6:] == '_2.tif':
		mosaicList.append(r)

mosaic2000 = [mosaicList[0], mosaicList[1]]
mosaic2001 = [mosaicList[2], mosaicList[3]]
mosaicSets = [mosaic2000, mosaic2001]
i = 0
for i in range(len(mosaicSets)):
	mosaic(mosaicSets[i])
	i += 1
###

###
#Clip Each NDVI raster by the extent of the Kastens et al (2017) data
directory = "D:\\AgIntensificationData\\ndvi\\"
clipper = "D:\\AgIntensificationData\\Data_Processing\\rasterClipperKastens.img"
clipperRaster = Raster("D:\\AgIntensificationData\\Data_Processing\\rasterClipperKastens.img")
rootList = []
directoryList = []
fileList = []

#Set up os.walk to get a list of all of the file directories from which I want to clip rasters
for root, directories, filenames in os.walk(directory):
	rootList.append(root)
	directoryList.append(directories)
	fileList.append(filenames)
#The list needs to start at the second item, because the first is a directory that is one level up from what I need
rootList = rootList[1:]

#Create a raster list from each of the directories, then clip the rasters.
for root in rootList:
	arcpy.env.workspace = root
	print "the current directory is: " + root
	rasterList = arcpy.ListRasters()
	rasterList2 = [i for i in rasterList if len(i) <= 12]
	for r in rasterList2:
		print "clipping raster: " + r
		outName = r[:-4] + '_clip' + r[-4:]
		raster1 = Raster(os.path.join(root, r))
		rasterOutput = clipperRaster * raster1
		rasterOutput.save(os.path.join("D:\\AgIntensificationData\\Data_Processing\\", outName))
arcpy.CheckInExtension("Spatial")
###
"""

###
#Reclassify each of the Kastens LandCover images to five classes
#1-SoyDouble, 2-SoySingle, 3-Pasture/Savanna, 4-Forest, 0-Other
ws = "D:\\AgIntensificationData\\Kastens_landCover\\"
arcpy.env.workspace = ws
rasterList = arcpy.ListRasters()
rasterList2 = [i for i in rasterList if i[:2] == "MT"]
for r in rasterList2:
	outName = "LC_Reclass_" + r[-8:-4] + "_1.img"
	print "reclassifying: " + r
	output = Reclassify(r, "Value", RemapValue([[1,1], [2,2], [3,0], [4,3], [5,4], [6,0], [7,0], [8,0], [9,0]]))
	output.save(os.path.join(ws, outName))
arcpy.CheckInExtension("Spatial")
