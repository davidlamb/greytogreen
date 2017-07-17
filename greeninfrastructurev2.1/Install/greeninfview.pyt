import arcpy

from g2gproject import Project
from sharedtools import sharedTools
import os
import sys
import cPickle as pickle

import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle




class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "greeninfview"
        self.alias = "greeninfview"

        # List of tool classes associated with this toolbox
        self.tools = [CreateProject,addFiles, copyProject, NHDSettings,CalculateAreas,matchLandcov,LoadProjectExcel,CreatePDFMap]
        arcpy.SetLogHistory(True)


class LoadProjectExcel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Open Project Excel"
        self.description = "Open the Grey to Green Workbook"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        return [configfile]

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            #os.startfile(_project.ProjectWorkbook)
            filename = _project.ProjectFolder + "\\" + _project.ProjectName + "_scenario.xlsm"
            if arcpy.Exists(filename):
                os.startfile(filename)
            else:
                arcpy.AddMessage("No scenario analysis tool found...")

class copyProject(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Copy Project Files"
        self.description = "Copy the original files from an existing project"
        self.canRunInBackground = False
    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        oldProject = arcpy.Parameter(
            displayName="Old Project File (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        currentProject = arcpy.Parameter(
            displayName="New ProjectFile (*.p)",
            name="newProjfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        return [oldProject,currentProject]
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        pass
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        pass
    def execute(self, parameters, messages):
        oldPath = parameters[0].valueAsText
        newPath = parameters[1].valueAsText
        _oldProject = pickle.load( open(oldPath, "rb" ) )
        _oldProject.updatePaths(os.path.dirname(newPath))
        pickle.dump(_oldProject,open(oldPath,'wb'))
        _newProject = pickle.load( open(newPath, "rb" ) )
        _newProject.updatePaths(os.path.dirname(newPath))
        pickle.dump(_newProject,open(newPath,'wb'))
        arcpy.AddMessage("Getting project files...")
        arcpy.AddMessage(_oldProject.ProjectDatabase)
        arcpy.AddMessage(_newProject.getBaseFilesDataset())
        lst = _oldProject.getFileOrgList()
        if lst == None:
            lst = []
        arcpy.AddMessage("Empty list....")
        _newProject.reviseFileOrg(lst)
        arcpy.AddMessage("Updating project settings...")
        sd = _oldProject.getSettingsDictionary()
        arcpy.AddMessage(sd)
        _newProject.updateSettings(sd)
        pickle.dump(_newProject,open(newPath,'wb'))
class CreatePDFMap(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create PDF Map"
        self.description = "Create PDF Map to Project Folder. Default is Portrait orientation."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        return [configfile]

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            #os.startfile(_project.ProjectWorkbook)
            _project.outputPDFMap()

class CreateProject(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "New Project"
        self.description = "Create a New Grey To Green Project"
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project Folder",
            name="ProjectFile",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        projname = arcpy.Parameter(
            displayName="Project Name",
            name="ProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        projsr = arcpy.Parameter(
            displayName="Project Spatial Reference",
            name="ProjectSR",
            datatype="GPSpatialReference",
            parameterType="Required",
            direction="Input"
        )

        projbnd = arcpy.Parameter(
            displayName="Project Boundaries",
            name="ProjectBND",
            datatype='GPFeatureLayer',
            parameterType="Required",
            direction="Input"
        )
        projbnd.filter.list = ["Polygon"]
        return [configfile,projname,projsr,projbnd]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        proj = Project()
        arcpy.AddMessage("toobox path:")
        arcpy.AddMessage(os.path.dirname(os.path.realpath(__file__)))
        proj.ProjectFolder = parameters[0].valueAsText
        proj.ProjectName = parameters[1].valueAsText.replace(" ","_")
        sr = parameters[2].value
        v = parameters[3].value
        if hasattr(v, 'dataSource'):
            proj.ProjectBoundsOrigPath = v.dataSource
        elif hasattr(v, 'name'):
            proj.ProjectBoundsOrigPath = v.name
        else:
            proj.ProjectBoundsOrigPath = str(v)
        proj.ProjectSpatialRefCode = sr.factoryCode

        arcpy.AddMessage("Project Folder and Name:")
        arcpy.AddMessage(proj.ProjectFolder)
        arcpy.AddMessage(proj.ProjectName)
        arcpy.AddMessage(proj.ProjectSpatialRefCode)
        arcpy.AddMessage(proj.ProjectBoundsOrigPath)

        if proj.createProject():
            arcpy.AddMessage(proj.ProjectDatabase)
            arcpy.AddMessage(proj.ProjectSpatialRefCode)
            arcpy.AddMessage(proj.ProjectBoundsDBPath)
            arcpy.AddMessage(proj.ProjectWorkbook)
            unique_name = arcpy.CreateUniqueName(proj.ProjectName +".p",proj.ProjectFolder)
            pickle.dump(proj,open(unique_name,'wb'))
            return
        else:
            arcpy.AddError("Failed to create project")


class addFiles(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Files to Project"
        self.description = "Add Required Files to the Project Database"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        fileInput = arcpy.Parameter(
            displayName = "Feature or Raster Layer to Add",
            name = "featrastlayer",
            datatype = ['DERasterDataset','DEFeatureClass',],
            parameterType="Optional",
            direction="Input")

        fileTypes = arcpy.Parameter(
            displayName = "Type of File",
            name = "typeoffile",
            datatype = 'GPString',
            parameterType="Optional",
            direction="Input")
        fileTypes.filter.type = "ValueList"
        fileTypes.filter.list = ["Load your project first"]

        fileswithtype = arcpy.Parameter(
            displayName='Selected Files',
            name='in_features',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input')
        fileswithtype.columns = [['String', 'Features'], ['String', 'Type']]

        errorp = arcpy.Parameter(
            displayName = "Errors",
            name = "errors",
            datatype = 'GPString',
            parameterType="Optional",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName = "Elevation Units",
            name = "eunits",
            datatype = 'GPString',
            parameterType="Optional",
            direction="Input")
        param1.filter.type = "ValueList"
        param1.filter.list = ['Feet','Meters']

        param2 = arcpy.Parameter(
            displayName = "Drainage Area in Acres",
            name = "darea",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param2.value = 0.0

        param3 = arcpy.Parameter(
            displayName = "Protective Buffer (Feet)",
            name = "pbuffer",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param3.value = 0.0

        param4 = arcpy.Parameter(
            displayName = "Percent Tree Canopy Cutoff (Percentage)",
            name = "ptreecanopy",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param4.value = 0.0



        param5 = arcpy.Parameter(
            displayName = "Steep Slope (%)",
            name = "pslope",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param5.value = 0.0


        param6 = arcpy.Parameter(
            displayName = "Percent Impervious Canopy Cutoff (Percentage)",
            name = "pimp",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param6.value = 0.0
        return [configfile,fileInput, fileTypes,fileswithtype,param1,param2,param3,param4,param5,param6]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        try:
            if arcpy.CheckExtension("Spatial") != "Available":
                raise Exception
        except Exception:
            return False  # tool cannot be executed


        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if not parameters[0].value:
            global previousPath2
            previousPath2 = ""
            global fileTypes
            fileTypes = {}


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        _project = Project()
        global fileTypes
        if parameters[0].altered:
            path = parameters[0].valueAsText


            if not arcpy.Exists(path):
                parameters[0].setErrorMessage("Does not exist!")

            global previousPath2
            if previousPath2 != path:
                previousPath2 = path
                _project = pickle.load( open(path, "rb" ) )
                _project.updatePaths(os.path.dirname(path))
                pickle.dump(_project,open(path,'wb'))
                try:
                    mxd = arcpy.mapping.MapDocument("CURRENT")
                    if mxd:
                        if mxd.filePath != '' and mxd.filePath == _project.ProjectDocument:
                            parameters[0].setErrorMessage("Please close the project Map Document. This tool will need access to this file: %s"%mxd.filePath)
                            raise arcpy.ExecuteError
                except:
                    pass
                if _project:

                    fileTypes = _project.getFileTypesDictionary()
                    settings = _project.getSettingsDictionary()
                    parameters[2].filter.list = sorted(fileTypes.keys())
                    parameters[3].values = _project.getFileOrgList()
                    parameters[4].value = settings[parameters[4].displayName]
                    parameters[5].value = settings[parameters[5].displayName]
                    parameters[6].value = settings[parameters[6].displayName]
                    parameters[7].value = settings[parameters[7].displayName]
                    parameters[8].value = settings[parameters[8].displayName]
                    parameters[9].value = settings[parameters[9].displayName]
            if parameters[2].altered and parameters[1].altered:
                lol = parameters[3].values
                newFeature = parameters[1].valueAsText
                newType = parameters[2].valueAsText
                global fileTypes
                if not lol:
                    lol = []
                addBool = True
                for x in lol:
                    exFeature = x[0]
                    exType = x[1]
                    if exFeature == newFeature:
                        addBool = False
                    if exType == newType:
                        addBool = False
                if addBool:
                    try:
                        requiredType = fileTypes[newType]['geom']
                        if requiredType == 'Raster':
                            if sharedTools.isRaster(newFeature):
                                lol.append([newFeature,newType])
                                parameters[3].values = lol
                                parameters[1].value =""
                                parameters[2].value = ""
                            else:
                                parameters[3].setErrorMessage("This type requires a %s layer"%(requiredType))
                        else:
                            if sharedTools.isVector(newFeature):
                                desc = arcpy.Describe(newFeature)
                                if requiredType == desc.shapeType:
                                    requiredField = requiredType = fileTypes[newType]['field']
                                    if requiredField !="None":

                                        fields = [f.name.upper() for f in arcpy.ListFields(newFeature)]
                                        if requiredField.upper() in fields:
                                            lol.append([newFeature,newType])
                                            parameters[3].values = lol
                                            parameters[1].value =""
                                            parameters[2].value = ""
                                        else:
                                            parameters[3].setErrorMessage("Missing required field %s"%(requiredField))
                                    else:
                                        lol.append([newFeature,newType])
                                        parameters[3].values = lol
                                        parameters[1].value =""
                                        parameters[2].value = ""
                                else:
                                    parameters[3].setErrorMessage("Expected a layer of type %s"%(requiredType))
                    except:
                        pass
                else:
                    parameters[3].values = lol
            del _project
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText
        arcpy.AddMessage(parameters[3].values)

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            arcpy.AddMessage(_project.ProjectDatabase)
            arcpy.AddMessage(_project.getBaseFilesDataset())
        #     fileOrgTable = _project.getFileOrgTablePath()
        #     existingList = _project.getFileOrgList()
        #     repeatedValues = []
        #     for i,j in enumerate(parameters[3].values):
        #         if j in existingList:
        #             repeatedValues.append(i)
        #     arcpy.AddMessage(repeatedValues)
        #
        # #arcpy.DeleteRows_management(fileOrgTable)
        #
        #     with arcpy.da.InsertCursor(fileOrgTable,_project.getFileOrgTableFields()) as inc:
        #         for ind,val in enumerate( parameters[3].values):
        #             if ind not in repeatedValues:
        #                 desc = arcpy.Describe(val[0])
        #                 bn = desc.baseName
        #                 newDBPath = arcpy.CreateUniqueName(bn,_project.getBaseFilesDataset())
        #                 arcpy.AddMessage(newDBPath)
        #                 newLoc = arcpy.CopyFeatures_management(val[0],newDBPath)[0]
        #                 inc.insertRow([val[1],newLoc,val[0]]).
            lst = parameters[3].values
            if lst == None:
                lst = []
            _project.reviseFileOrg(lst)
            sd = {parameters[4].displayName:parameters[4].value,parameters[5].displayName:parameters[5].value,
                  parameters[6].displayName:parameters[6].value,parameters[7].displayName:parameters[7].value,
                  parameters[8].displayName:parameters[8].value,parameters[9].displayName:parameters[9].value}
            _project.updateSettings(sd)
            pickle.dump(_project,open(path,'wb'))

        global previousPath2
        previousPath2 = ""
        global fileTypes
        fileTypes = {}


class NHDSettings(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NHD Settings"
        self.description = "Modify settings for handling NHD datasets"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")


        param0 = arcpy.Parameter(
            displayName="NHD Flow lines",
            name="NHDFlowline",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        param1 = arcpy.Parameter(
            displayName="NHD Points",
            name="NHDPoint",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        param2 = arcpy.Parameter(
            displayName="NHD Waterbodies",
            name="NHDWaterbody",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        param3 = arcpy.Parameter(
            displayName="NHD Areas",
            name="NHDArea",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        return [configfile,param0,param1,param2,param3]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if not parameters[0].value:
            global previousPath2
            previousPath2 = ""
            global fileTypes
            fileTypes = {}


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        _project = Project()

        if parameters[0].altered:
            path = parameters[0].valueAsText
            if not arcpy.Exists(path):
                parameters[0].setErrorMessage("Does not exist!")
            global previousPath2
            if previousPath2 != path:
                previousPath2 = path
                _project = pickle.load( open(path, "rb" ) )
                _project.updatePaths(os.path.dirname(path))
                pickle.dump(_project,open(path,'wb'))
                if _project:
                    values = _project.getNHDFeatureTypes()
                    for i in range(1,5):
                        parameters[i].filter.list = [x[0] for x in values[parameters[i].name]]
                        parameters[i].value = [x[0] for x in values[parameters[i].name] if x[1] ]


            del _project
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            values = []
            for i in range(1,5):
                vat = parameters[i].valueAsText
                values += vat.split(";")
            values = [x.replace("'","") for x in values]
            _project.updateActiveNHDFeatureTypes(values)
            pickle.dump(_project,open(path,'wb'))

        global previousPath2
        previousPath2 = ""


class CalculateAreas(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Green Infrastructure"
        self.description = "Calcualte the Green Infrastructure Map, and potential areas"
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName = "Estimated Existing Rooftop Impervious Coverage (Square Feet)",
            name = "estimate1",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param2.value = 0.0

        param3 = arcpy.Parameter(
            displayName = "Estimated Existing Non-Rooftop Impervious Coverage (Square Feet)",
            name = "estimate2",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param3.value = 0.0

        param4 = arcpy.Parameter(
            displayName = "Estimated Proposed  Rooftop Impervious Coverage (Square Feet)",
            name = "estimate3",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param4.value = 0.0

        param5 = arcpy.Parameter(
            displayName = "Estimated Proposed Non-Rooftop Impervious Coverage (Square Feet)",
            name = "estimate4",
            datatype = 'GPDouble',
            parameterType="Optional",
            direction="Input")
        param5.value = 0.0

        bmpList = arcpy.Parameter(
            displayName="Select BMP",
            name="bmpList",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        thisModPath = os.path.realpath(__file__)
        thisModPath = os.path.dirname(thisModPath)
        basedb = os.path.join(thisModPath,"basedb.gdb")
        domainList = arcpy.da.ListDomains(basedb)
        bv = []
        for d in domainList:
            if d.name.lower() == "bmpname":
                for val, desc in d.codedValues.iteritems():
                    bv.append(val)
        bmpList.filter.type = "ValueList"
        bmpList.filter.list = bv

        #return [configfile,param2,param3,param3,param4,bmpList]
        return [configfile]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[0].altered:
            path = parameters[0].valueAsText


            if not arcpy.Exists(path):
                parameters[0].setErrorMessage("Does not exist!")
            else:
                _project = pickle.load( open(path, "rb" ) )
                _project.updatePaths(os.path.dirname(path))
                pickle.dump(_project,open(path,'wb'))
                try:
                    mxd = arcpy.mapping.MapDocument("CURRENT")
                    if mxd:
                        if mxd.filePath != '' and mxd.filePath == _project.ProjectDocument:
                            parameters[0].setErrorMessage("Please close the project Map Document. This tool will need access to this file: %s"%mxd.filePath)
                            raise arcpy.ExecuteError
                except:
                    pass
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText
        arcpy.AddMessage(path)
        #selectedBMPS = parameters[5].values
        #arcpy.AddMessage(selectedBMPS)a
        pass
        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            arcpy.AddMessage(os.path.dirname(path))
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            "=========Calculate Green Infrastructure Map========="
            _project.createAreasTable()
            _project.clearValues()
            _project.writeGIM()
            "=========Calculate Site Locations========="
            #_project.calculateCriteriaAreas(selectedBMPS)
            _project.calculateCriteriaAreasNew()
            "=========Calculate Impervious and Pervious====="
            _project.imperviousPerviousAreas()
            #_project.treesWithinImperviousPervious()
            #_project.perviousWithSoil()
            #_project.writePerviousAreas()
            #"=========Calculate Tree Areas within Impervious Areas====="
            #_project.createCreditsTable()
            #_project.treesWithinImpervious()
            #_project.writeCreditAreas()
           # arcpy.AddMessage("Write Areas to Text File")
            #_project.writeOutCurrentAreas()
            _project.writeOutCurrentAreas()
            arcpy.AddMessage("Open Excel")
            #writeout to excel file
            os.startfile(_project.ProjectWorkbook)
            arcpy.AddMessage("=========Cleaning Up=========")
            _project.cleanupDeleteList()
            arcpy.AddMessage("=========Open Map Document=========")
            os.startfile(_project.ProjectDocument)
            pickle.dump(_project,open(path,'wb'))


            #create a table to store the areas, give it a unique name

class CalculateCredits(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Credits"
        self.description = "Create the credits table"
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")


        return [configfile]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText
        arcpy.AddMessage(path)

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            _project.createCreditsTable()
            pickle.dump(_project,open(path,'wb'))
            #arcpy.AddMessage("Write Areas to Text File")
            #_project.writeOutCurrentAreas()
           #arcpy.AddMessage("Open Excel")
            #os.startfile(_project.ProjectWorkbook)
            #arcpy.AddMessage("=========Cleaning Up=========")
           # _project.cleanupDeleteList()
            #arcpy.AddMessage("=========Open Map Document=========")
            #os.startfile(_project.ProjectDocument)


            #create a table to store the areas, give it a unique name



class matchLandcov(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Match landcover classifications"
        self.description = "Matches a landcover dataset to those used in the tools."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        fileInput = arcpy.Parameter(
            displayName = "Input Raster Layer Landcover",
            name = "featrastlayer",
            datatype = ['DERasterDataset'],
            parameterType="Optional",
            direction="Input")

        fileTypes = arcpy.Parameter(
            displayName = "Defined Landcover Types",
            name = "typeoffile",
            datatype = 'GPString',
            parameterType="Optional",
            direction="Input",)
        fileTypes.filter.type = "ValueList"
        fileTypes.filter.list = ["Load your project first"]

        landcovTypes = arcpy.Parameter(
            displayName = "Existing Landcover Types",
            name = "landcovtypes",
            datatype = 'GPString',
            parameterType="Optional",
            direction="Input",
            multiValue=True)
        landcovTypes.filter.type = "ValueList"
        landcovTypes.filter.list = ["Load your raster file first"]

        fileswithtype = arcpy.Parameter(
            displayName='Selected Files',
            name='in_features',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input')
        fileswithtype.columns = [['String', 'Existing Landcover Types'], ['String', 'Defined Landcover Types']]



        return [configfile,fileInput,landcovTypes,fileTypes,fileswithtype]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if not parameters[0].value:
            global previousLandcovPath
            previousLandcovPath = ""

            global previousProjectPath3
            previousProjectPath3 = ""


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        _project = Project()
        global fileTypes
        if parameters[0].altered:
            path = parameters[0].valueAsText
            if not arcpy.Exists(path):
                parameters[0].setErrorMessage("Does not exist!")

                #with arcpy.da.SearchCursor("nlcd_2006_landcover_2011_edition_2014_10_10.img", ["VALUE"]) as cursor:
            #...     values = sorted({row[0] for row in cursor})
            global previousProjectPath3
            if previousProjectPath3 != path:
                previousProjectPath3 = path
                _project = pickle.load( open(path, "rb" ) )
                _project.updatePaths(os.path.dirname(path))
                pickle.dump(_project,open(path,'wb'))
                if _project:
                    matchLandcov = _project.getlandcoverValuesToMatch()
                    parameters[3].filter.list = sorted(matchLandcov)

            if parameters[1].altered:
                rasterLayer = parameters[1].valueAsText
                global previousLandcovPath
                if previousLandcovPath != rasterLayer:
                    previousLandcovPath = rasterLayer
                    with arcpy.da.SearchCursor(rasterLayer, ["VALUE"]) as cursor:
                        values = sorted({row[0] for row in cursor})
                    parameters[2].filter.list = values

            if parameters[2].altered and parameters[3].altered:
                currentValues = parameters[4].values
                newExisting = parameters[2].valueAsText
                matchedTo = parameters[3].valueAsText
                if matchedTo and newExisting:
                    if matchedTo != "" and len(newExisting)!=0:
                        if not currentValues:
                            currentValues = []
                        addBool = True
                        for x in currentValues:
                            exFeature = x[1]
                            if exFeature == matchedTo:
                                addBool = False
                        if addBool:
                            currentValues.append([matchedTo,newExisting])
                            parameters[4].values = currentValues

                        #done
                            parameters[2].values = []
                            parameters[3].value = ""

            #     global fileTypes
            #     if not lol:
            #         lol = []
            #     addBool = True
            #     for x in lol:
            #         exFeature = x[0]
            #         exType = x[1]
            #         if exFeature == newFeature:
            #             addBool = False
            #         if exType == newType:
            #             addBool = False
            #     if addBool:
            #         requiredType = fileTypes[newType]['geom']
            #         if requiredType == 'Raster':
            #             if sharedTools.isRaster(newFeature):
            #                 lol.append([newFeature,newType])
            #                 parameters[3].values = lol
            #             else:
            #                 parameters[3].setErrorMessage("This type requires a %s layer"%(requiredType))
            #         else:
            #             if sharedTools.isVector(newFeature):
            #                 desc = arcpy.Describe(newFeature)
            #                 if requiredType == desc.shapeType:
            #                     requiredField = requiredType = fileTypes[newType]['field']
            #                     if requiredField !="None":
            #
            #                         fields = [f.name.upper() for f in arcpy.ListFields(newFeature)]
            #                         if requiredField.upper() in fields:
            #                             lol.append([newFeature,newType])
            #                             parameters[3].values = lol
            #                         else:
            #                             parameters[3].setErrorMessage("Missing required field %s"%(requiredField))
            #                     else:
            #                         lol.append([newFeature,newType])
            #                         parameters[3].values = lol
            #                 else:
            #                     parameters[3].setErrorMessage("Expected a layer of type %s"%(requiredType))
            #     else:
            #         parameters[3].values = lol
            del _project
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            currentValues = parameters[4].values
            insertDict = {}
            for val in currentValues:
                code = val[0].split("|")[0]
                values = val[1].split(";")
                insertDict[code] = values
            arcpy.AddMessage(insertDict)
            _project.updateLandcoverMatchCode(insertDict)
            pickle.dump(_project,open(path,'wb'))
            del _project

        global previousLandcovPath
        previousLandcovPath = ""

        global previousProjectPath3
        previousProjectPath3 = ""



class CalculatePerviousSoil(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Pervious Soil Areas"
        self.description = "Find Intersection Pervious and Pervious No Forest Areas with Soil Hydrologic Group"
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        configfile = arcpy.Parameter(
            displayName="Project File to Modify (*.p)",
            name="projectfile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        return [configfile]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        path = parameters[0].valueAsText
        arcpy.AddMessage(path)

        if arcpy.Exists(path):
            _project = pickle.load( open(path, "rb" ) )
            _project.updatePaths(os.path.dirname(path))
            pickle.dump(_project,open(path,'wb'))
            _project.perviousWithSoil()
            #_project.writeOutAreas()
            pickle.dump(_project,open(path,'wb'))
            #arcpy.AddMessage("Write Areas to Text File")
            #_project.writeOutCurrentAreas()
           #arcpy.AddMessage("Open Excel")
            #os.startfile(_project.ProjectWorkbook)
            #arcpy.AddMessage("=========Cleaning Up=========")
           # _project.cleanupDeleteList()
            #arcpy.AddMessage("=========Open Map Document=========")
            #os.startfile(_project.ProjectDocument)


            #create a table to store the areas, give it a unique name