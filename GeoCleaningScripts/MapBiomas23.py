#Process the MapBiomas 2.3 data

#import modules
import arcpy
import os
from arcpy.sa import *
import string

#Workspace
arcpy.env.overwriteOutput = True
ws = "D:\\GISData_PostPhD\\MapBiomas_v23\\OriginalData\\"
arcpy.env.workspace = ws
arcpy.CheckOutExtension("Spatial")

#Export each raster band as a new .tif file
def rasterBand(bandCount):
	rasterList = arcpy.ListRasters()
	for r in range(len(rasterList)):
		count = 1
		for i in range(len(bandCount)):
			TifToLoad = ws + rasterList[r] + "\\Band_" + str(count)
			year = (count - 1) + 2000
			name1 = rasterList[r][:-4]
			name2 = name1 + "_" + str(year) + ".tif"
			arcpy.CopyRaster_management(TifToLoad, os.path.join("D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\", name2), 
			"", "", "0", "", "", "8_BIT_SIGNED", "", "", "", "")
			print "Copying " + name2
			count += 1

#Convert to Integer
def Integer(ws):
	arcpy.env.workspace = ws
	print "arc workspace is: " + ws
	rasterList = arcpy.ListRasters()
	for r in rasterList:
		name = r[:-4]
		outName = name + "_int" + ".tif"
		print "calculating " + name + " as integer."
		outInt = Int(r)
		outInt.save(os.path.join("D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\", outName))

#Mosaic biomes together for each year
def mosaicRasters(raster_list, year):
	year = str(year)
	outputLocation = "D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\"
	print "Mosaicking " + raster_list + " together..."
	arcpy.MosaicToNewRaster_management(raster_list, outputLocation, "BrazilLC_" + year + "_30m.img", "4326", "8_BIT_SIGNED", "", "1", "LAST", "FIRST")
	print "Mosaic raster created for year: " + year

#Convert to Integer
def Integer2(ws):
	arcpy.env.workspace = ws
	print "arc workspace is: " + ws
	rasterList = arcpy.ListDatasets("*Brazil*", "Raster")
	for r in rasterList:
		name = r[:-4]
		outName = name + "_int" + ".img"
		print "calculating " + name + " as integer."
		outInt = Int(r)
		outInt.save(os.path.join("D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\", outName))

#Reclassify
def reclassifyRasters(ws):
	arcpy.env.workspace = ws
	print "arc workspace is: " + ws
	rasterList = arcpy.ListDatasets("*30m_int*", "Raster")
	rasterList2 = rasterList[11:]
	print "rasterList2: " + ''.join(rasterList2)
	for r in rasterList2:
		name = r[:-4]
		outName = name + "_reclass.img"
		print "reclassifying " + name
		output = Reclassify(r, "Value", RemapValue([[1,1], [2,1], [3,1], [4,1], [5,1], [9,1], [10,1], [11,1], [12,1], [13,1], [14,3], [15,2], [18,3], [21,2], [22,4], [23,4], [24,4], [25,4], [26,4], [27,2]]))
		output.save(os.path.join("D:\\GISData_PostPhD\\MapBiomas_v23\\James\\Reclassified_Images\\", outName))


#Local variables and functions
bandCount = ["1", "2", "3", "4", "5", "6", 
		"7", "8", "9", "10", "11", "12", 
		"13", "14", "15", "16", "17"]

##Run the rasterBand function
#rasterBand(bandCount)
##Change the workspace and run the Integer function
#ws = "D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\"
#Integer(ws)

##Prepare the data for the Mosaic function
"""
year = 2008
ws = "D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\"
arcpy.env.workspace = ws
print "arc workspace is: " + ws
rasterList = arcpy.ListDatasets("*_int*", "Raster")
while year <= 2016:
	list_year = []
	for r in rasterList:
		if str(year) in r:
			list_year.append(r)
	list_year = ','.join(list_year)
	list_year = list_year.replace(",", ";")
	raster_list = list_year.encode('ascii', 'ignore')
	raster_list = '"' + raster_list + '"'
	print "the biomes that will be mosaicked together are: " + raster_list
	
	#Call the Mosaic function
	mosaicRasters(raster_list, year)
	year += 1
"""

##Change workspace and call the Integer2 function again
#ws = "D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\"
#Integer2(ws)

#Call the Reclassify function
ws = "D:\\GISData_PostPhD\\MapBiomas_v23\\Year_Exports\\Processing\\"
reclassifyRasters(ws)