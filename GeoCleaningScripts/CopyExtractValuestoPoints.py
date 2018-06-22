#This script was produced to select points by FID, then copy these shapefiles, then extract all raster values to points for the 
#Agricultural Intensification paper based on the Kastens et al (2017) data.
#This process ensures that values across multiple raster files are consistently
#placed in the correct geospatial position.
#Author: Paul McCord, Date Created: 4-19-18

#Import modules
import arcpy
from arcpy.sa import *
import os
import string

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
ws = "D:\\AgIntensificationData\\Analysis\\processing"
arcpy.env.workspace = ws


#Select by Attribute Function
def selectByAtt(feature, i):
	arcpy.MakeFeatureLayer_management(feature, "lyr_" + str(i))
	arcpy.SelectLayerByAttribute_management("lyr_" + str(i), "NEW_SELECTION", '"FID" <= 490574')
	copy1 = arcpy.CopyFeatures_management("lyr_" + str(i), feature[:-4] + '_' + str(i) + '_1' + feature[-4:])
	copyList.append(copy1)
	arcpy.SelectLayerByAttribute_management("lyr_" + str(i), "NEW_SELECTION", '"FID" >= 490575 AND "FID" <= 981148')
	copy2 = arcpy.CopyFeatures_management("lyr_" + str(i), feature[:-4] + '_' + str(i) + '_2' + feature[-4:])
	copyList.append(copy2)
	arcpy.SelectLayerByAttribute_management("lyr_" + str(i), "NEW_SELECTION", '"FID" >= 981149 AND "FID" <= 1471722')
	copy3 = arcpy.CopyFeatures_management("lyr_" + str(i), feature[:-4] + '_' + str(i) + '_3' + feature[-4:])
	copyList.append(copy3)
	arcpy.SelectLayerByAttribute_management("lyr_" + str(i), "NEW_SELECTION", '"FID" >= 1471723')
	copy4 = arcpy.CopyFeatures_management("lyr_" + str(i), feature[:-4] + '_' + str(i) + '_4' + feature[-4:])
	copyList.append(copy4)
	print "selected and exported from group " + str(i) + " " + feature

#Get the list of shapefiles that will be used in the analysis
fC = arcpy.ListFeatureClasses()
fC2 = [i for i in fC if len(i) == 15]

#This list will be used to copy each point feature class
copyList = []

#Select by attributes
i = 0
print "beginning select by attributes"
for i in range(len(fC2)):
	feature = fC2[i]
	selectByAtt(feature, i)
	i += 1
print "completed select by attributes"


#Copy each of the shapefiles in the copyList
print "beginning the copying proceedure"
#Form a list of the shapefiles that will be included for copying
fcList = arcpy.ListFeatureClasses()
fcList2 = [i for i in fcList if "copy" not in i and len(i) > 15]
#Copy
for fc in fcList2:
	outName = fc[:-4] + '_copy2' + fc[-4:]
	print "copying " + fc
	arcpy.CopyFeatures_management(fc, os.path.join(ws, outName))


#Run the Extract Multi Values to Points tool
#Form a list of the shapefiles that will be used as the set of points
extractList = arcpy.ListFeatureClasses()
extractList2 = [i for i in extractList if i[-9:-4] == "copy2"]
#I ran the tool successfully for the first feature class in this list, so skip this feature class:
extractList3 = extractList2[1:]
ws = "D:\\AgIntensificationData\\Data_Processing"
arcpy.env.workspace = ws
print "extracting values to points"
#Extract Multivalues to Points
shapefilePath = "D:\\AgIntensificationData\\Analysis\\processing"
i = 0
for i in range(len(extractList3)):
	ExtractMultiValuesToPoints(os.path.join(shapefilePath, extractList3[i]), [["LC_Reclass_2001_1.img", "LC_2001"],
																			["LC_Reclass_2002_1.img", "LC_2002"],
																			["LC_Reclass_2003_1.img", "LC_2003"],
																			["LC_Reclass_2004_1.img", "LC_2004"],
																			["LC_Reclass_2005_1.img", "LC_2005"],
																			["LC_Reclass_2006_1.img", "LC_2006"],
																			["LC_Reclass_2007_1.img", "LC_2007"],
																			["LC_Reclass_2008_1.img", "LC_2008"],
																			["LC_Reclass_2009_1.img", "LC_2009"],
																			["LC_Reclass_2010_1.img", "LC_2010"],
																			["LC_Reclass_2011_1.img", "LC_2011"],
																			["LC_Reclass_2012_1.img", "LC_2012"],
																			["LC_Reclass_2013_1.img", "LC_2013"],
																			["LC_Reclass_2014_1.img", "LC_2014"],
																			["00rs1Avg_clip.tif", "i00VIrs1Av"],
																			["00rs1Var_clip.tif", "i00VIrs1Va"],
																			["00rsAvg_clip.tif", "i00VIrsAv"],
																			["00rsVar_clip.tif", "i00VIrsVa"],
																			["01rs1Avg_clip.tif", "i01VIrs1Av"],
																			["01rs1Var_clip.tif", "i01VIrs1Va"],
																			["01rsAvg_clip.tif", "i01VIrsAv"],
																			["01rsVar_clip.tif", "i01VIrsVa"],
																			["02rs1Avg_clip.tif", "i02VIrs1Av"],
																			["02rs1Var_clip.tif", "i02VIrs1Va"],
																			["02rsAvg_clip.tif", "i02VIrsAv"],
																			["02rsVar_clip.tif", "i02VIrsVa"],
																			["03rs1Avg_clip.tif", "i03VIrs1Av"],
																			["03rs1Var_clip.tif", "i03VIrs1Va"],
																			["03rsAvg_clip.tif", "i03VIrsAv"],
																			["03rsVar_clip.tif", "i03VIrsVa"],
																			["04rs1Avg_clip.tif", "i04VIrs1Av"],
																			["04rs1Var_clip.tif", "i04VIrs1Va"],
																			["04rsAvg_clip.tif", "i04VIrsAv"],
																			["04rsVar_clip.tif", "i04VIrsVa"],
																			["05rs1Avg_clip.tif", "i05VIrs1Av"],
																			["05rs1Var_clip.tif", "i05VIrs1Va"],
																			["05rsAvg_clip.tif", "i05VIrsAv"],
																			["05rsVar_clip.tif", "i05VIrsVa"],
																			["06rs1Avg_clip.tif", "i06VIrs1Av"],
																			["06rs1Var_clip.tif", "i06VIrs1Va"],
																			["06rsAvg_clip.tif", "i06VIrsAv"],
																			["06rsVar_clip.tif", "i06VIrsVa"],
																			["07rs1Avg_clip.tif", "i07VIrs1Av"],
																			["07rs1Var_clip.tif", "i07VIrs1Va"],
																			["07rsAvg_clip.tif", "i07VIrsAv"],
																			["07rsVar_clip.tif", "i07VIrsVa"],
																			["08rs1Avg_clip.tif", "i08VIrs1Av"],
																			["08rs1Var_clip.tif", "i08VIrs1Va"],
																			["08rsAvg_clip.tif", "i08VIrsAv"],
																			["08rsVar_clip.tif", "i08VIrsVa"],
																			["09rs1Avg_clip.tif", "i09VIrs1Av"],
																			["09rs1Var_clip.tif", "i09VIrs1Va"],
																			["09rsAvg_clip.tif", "i09VIrsAv"],
																			["09rsVar_clip.tif", "i09VIrsVa"],
																			["10rs1Avg_clip.tif", "i10VIrs1Av"],
																			["10rs1Var_clip.tif", "i10VIrs1Va"],
																			["10rsAvg_clip.tif", "i10VIrsAv"],
																			["10rsVar_clip.tif", "i10VIrsVa"],
																			["11rs1Avg_clip.tif", "i11VIrs1Av"],
																			["11rs1Var_clip.tif", "i11VIrs1Va"],
																			["11rsAvg_clip.tif", "i11VIrsAv"],
																			["11rsVar_clip.tif", "i11VIrsVa"],
																			["12rs1Avg_clip.tif", "i12VIrs1Av"],
																			["12rs1Var_clip.tif", "i12VIrs1Va"],
																			["12rsAvg_clip.tif", "i12VIrsAv"],
																			["12rsVar_clip.tif", "i12VIrsVa"],
																			["13rs1Avg_clip.tif", "i13VIrs1Av"],
																			["13rs1Var_clip.tif", "i13VIrs1Va"],
																			["13rsAvg_clip.tif", "i13VIrsAv"],
																			["13rsVar_clip.tif", "i13VIrsVa"],
																			["14rs1Avg_clip.tif", "i14VIrs1Av"],
																			["14rs1Var_clip.tif", "i14VIrs1Va"],
																			["14rsAvg_clip.tif", "i14VIrsAv"],
																			["14rsVar_clip.tif", "i14VIrsVa"],
																			["elevation_SRTM_clip_250.img", "elev"],
																			["slope.img", "slope"],
																			["soils_70classes.img", "soil_type"],
																			["CostDistance_toUrban_1.img", "CosDisUrb"],
																			["EuclideanDistance_toUrban_1.img", "EucDisUrb"],
																			["CostDistance_toRoads_1.img", "CosDisRds"],
																			["EuclideanDistance_toRoads_1.img", "EucDisRds"]])
	print "extracted values to points for " + str(i) + " shapefile"
	i += 1

arcpy.CheckInExtension("Spatial")

print "the script has finished"
