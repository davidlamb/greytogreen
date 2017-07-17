import arcpy
import os
import glob

class SharedToolsError(Exception):
    pass



"""Shared tools stores constants, and static methods that may be used throughout. Mostly deals with unit conversions, and tests of data types"""
# TODO setup bmp type constants
class sharedTools(object):
    FOOT_US = 9003
    FOOT = 9002
    INCH = 109008
    INCH_US = 109009
    CENTIMETER = 109006
    KILOMETER = 109031
    MILE_US = 9035
    METER = 9001
    MILLIMETER = 109007
    DEGREE = 9102
    ELEVATION_UNITS = {"Feet":9003,"Meters":9001}
    GP_FEATURECLASS = "FeatureClass"
    GP_FEATURELAYER = "FeatureLayer"
    GP_SHAPEFILE = "ShapeFile"
    GP_RASTERDATASET = "RasterDataset"
    GP_RASTERLAYER = "RasterLayer"
    GP_DBASETABLE = "DbaseTable"
    GP_TABLE = "Table"
    GP_FOLDER = "Folder"
    GP_POLYGON_ST = "Polygon"
    GP_POLYLINE_ST = "Polyline"
    GP_POINT_ST = "Point"
    GP_MULTIPOINT_ST = "MultiPoint"
    GP_MULTIPATCH_ST = "MultiPatch"
    SOIL_GROUP_L = ["A","B","C","D"]


    @staticmethod
    def reportErrortoArcpy(message):
        arcpy.AddMessage(message)
        arcpy.AddError(message)


    @staticmethod
    def incrementName(workspace,name):


        path = workspace + "\\" + name + "*"

        if len(glob.glob(path))==0:
            return name
        else:
            tester = True
            incr = 1
            while tester:
                path = workspace + "\\" + name+str(incr)+ "*"
                if len(glob.glob(path))==0:
                    tester = False
                    return name+str(incr)
                incr+=1

    @staticmethod
    def prepareName(name):
        name = name.replace(" ","_")
        name = name[0:8]
        return name

    @staticmethod
    def getAcres(area,units):
        if "foot" in units.lower() or "feet" in units.lower():
            return area * 0.0000229568411
        elif "meter" in units.lower():
            return area * 0.00024711
        else:
            raise SharedToolsError("Not feet or meters in area conversion")


    @staticmethod
    def getFactorFromFeet(unitCode):
        if unitCode ==sharedTools.FOOT or unitCode == sharedTools.FOOT_US:
            return 1
        elif unitCode ==sharedTools.METER:
            return 0.3048
        elif unitCode ==sharedTools.INCH or unitCode == sharedTools.INCH_US:
            return 12
        elif unitCode ==sharedTools.CENTIMETER:
            return 30.48
        elif unitCode ==sharedTools.KILOMETER:
            return 0.0003048009
        elif unitCode == sharedTools.MILE_US:
            return 0.0001893939
        elif unitCode ==sharedTools.MILLIMETER:
            return 304.8
        elif unitCode == sharedTools.DEGREE:
            return 1.0
        else:
            raise SharedToolsError("Unknown linear unit code.")



    @staticmethod
    def zfactorConvertZtoLinear(horizontalUnitCode,verticalUnitCode):
        if horizontalUnitCode == verticalUnitCode:
            return 1.0
        else:
            if horizontalUnitCode == sharedTools.FOOT_US or horizontalUnitCode == sharedTools.FOOT:
                if verticalUnitCode == sharedTools.FOOT_US or verticalUnitCode == sharedTools.FOOT:
                    return 1.0
                if verticalUnitCode == sharedTools.METER:
                    return 3.28084
                if verticalUnitCode == sharedTools.DEGREE:
                    return 0.00001
            elif horizontalUnitCode == sharedTools.METER:
                 if verticalUnitCode == sharedTools.FOOT_US or verticalUnitCode == sharedTools.FOOT:
                     return 0.3048
                 if verticalUnitCode == sharedTools.DEGREE:
                    return 0.000003
            else:
                return 1.0

    @staticmethod
    def isRaster(datapath):
        arcpy.AddMessage("Datapath: %s"%datapath)
        datatype = arcpy.Describe(datapath).dataType
        if datatype == sharedTools.GP_RASTERDATASET:
            return True
        elif datatype == sharedTools.GP_RASTERLAYER:
            return True
        else:
            return False

    @staticmethod
    def isVector(datapath):
        datatype = arcpy.Describe(datapath).dataType
        if datatype == sharedTools.GP_FEATURECLASS:
            return True
        elif datatype == sharedTools.GP_FEATURELAYER:
            return True
        elif datatype == sharedTools.GP_SHAPEFILE:
            return True
        else:
            return False

    @staticmethod
    def isTable(datapath):
        datatype = arcpy.Describe(datapath).dataType
        if datatype == sharedTools.GP_DBASETABLE:
            return True
        elif datatype == sharedTools.GP_TABLE:
            return True
        else:
            return False
