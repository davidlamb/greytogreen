import arcpy
import pythonaddins
import math
import os
from subprocess import Popen
from os import listdir
from os.path import isfile, join

class AddFilesButton(object):
    """Implementation for greeninfrastructurev1_addin.AddFilesButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'addFiles')

class MapGIButton(object):
    """Implementation for greeninfrastructurev1_addin.MapGIButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'CalculateAreas')

class NewProjectButton(object):
    """Implementation for greeninfrastructurev1_addin.NewProjectButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'CreateProject')

class buildingFeatureClass(object):
    """Implementation for greeninfrastructurev1_addin.buildingFeatureClass (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        save_full = pythonaddins.SaveDialog('Name for Buildings Layer', "buildings")
        save_full = os.path.normpath(save_full)
        save_file = os.path.basename(save_full)
        save_path = save_full.replace(save_file,"")
        mxd = arcpy.mapping.MapDocument('current')
        df = mxd.activeDataFrame
        sr = df.spatialReference
        if sr.name != '':
            if sr.type == 'Projected':
                createdFile = arcpy.CreateFeatureclass_management(save_path,save_file,"POLYGON",spatial_reference=sr)
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)


class projectBoundFeatureClass(object):
    """Implementation for greeninfrastructurev1_addin.buildingFeatureClass (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        save_full = pythonaddins.SaveDialog('Name for Project Boundary Layer', "projectbound")
        save_full = os.path.normpath(save_full)
        save_file = os.path.basename(save_full)
        save_path = save_full.replace(save_file,"")
        mxd = arcpy.mapping.MapDocument('current')
        df = mxd.activeDataFrame
        sr = df.spatialReference
        if sr.name != '':
            if sr.type == 'Projected':
                createdFile = arcpy.CreateFeatureclass_management(save_path,save_file,"POLYGON",spatial_reference=sr)
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

class comboArea(object):
    """Implementation for greeninfrastructurev1_addin.comboArea (ComboBox)"""
    def __init__(self):
        self.items = [2000, 2400, 5000, 50000]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.value = self.items[0]

    def onSelChange(self, selection):
        self.value = selection
    def onEditChange(self, text):
        self.value = text
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class comboWidth(object):
    """Implementation for greeninfrastructurev1_addin.comboArea (ComboBox)"""
    def __init__(self):
        self.items = [24,40,50,200]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = self.items[0]

    def onSelChange(self, selection):
        self.value = selection
    def onEditChange(self, text):
        self.value = text
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class comboHeight(object):
    """Implementation for greeninfrastructurev1_addin.comboArea (ComboBox)"""
    def __init__(self):
        self.items = [50,100,250]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = self.items[0]

    def onSelChange(self, selection):
        self.value = selection
    def onEditChange(self, text):
        self.value = text
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class comboWorkingLayer(object):
    """Implementation for greeninfrastructurev1_addin.workinglayer (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWW'
        self.width = 'WWWWWW'

    def onSelChange(self, selection):
        self.value = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        print focused
        # When the combo box has focus, update the combo box with the list of layer names.
        if focused:
            self.mxd = arcpy.mapping.MapDocument('current')
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items = []
            for layer in layers:
                if layer.isFeatureLayer:
                    desc = arcpy.Describe(layer.dataSource)
                    if desc.shapeType == "Polygon":
                        self.items.append(layer.name)
            self.value = self.items[0]


    def onEnter(self):
        pass
    def refresh(self):
        pass

class compactFeatureClass(object):
    """Implementation for greeninfrastructurev1_addin.compactFeatureClass (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        save_full = pythonaddins.SaveDialog('Name for Area of Minimum Compaction Layer', "mincompact")
        save_full = os.path.normpath(save_full)
        save_file = os.path.basename(save_full)
        save_path = save_full.replace(save_file,"")
        mxd = arcpy.mapping.MapDocument('current')
        df = mxd.activeDataFrame
        sr = df.spatialReference
        if sr.name != '':
            if sr.type == 'Projected':
                createdFile = arcpy.CreateFeatureclass_management(save_path,save_file,"POLYGON",spatial_reference=sr)
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

class featuretypesButton(object):
    """Implementation for greeninfrastructurev1_addin.featuretypesButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'NHDSettings')

class freeformTool(object):
    """Implementation for greeninfrastructurev1_addin.freeformTool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Line" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.array = arcpy.Array()

    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        try:
            layerName = workinglayer.value
        except:
            pythonaddins.MessageBox("Select Working Layer error.","Error",0)
            return None
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        layerds = lyr.dataSource
        dfsr = mxd.activeDataFrame.spatialReference
        if dfsr.name != '':
            if dfsr.type == 'Projected':
                desc = arcpy.Describe(layerds)
                layerSR = desc.spatialReference
                dfSR = mxd.activeDataFrame.spatialReference
                part = line_geometry.getPart(0)

                self.array = arcpy.Array()
                part = line_geometry.getPart(0)
                for pt in part:
                    self.array.add(pt)
                self.array.add(line_geometry.firstPoint)
                polygonOrig = arcpy.Polygon(self.array,dfSR,False,False)
                polygonOut = polygonOrig.projectAs(layerSR)


                ws = lyr.workspacePath
                edit = arcpy.da.Editor(ws)
                edit.startEditing(True,False)
                edit.startOperation()
                with arcpy.da.InsertCursor(layerds,["SHAPE@"])as ic:
                    ic.insertRow([polygonOut])

                arcpy.RefreshActiveView()

                if pythonaddins.MessageBox("Commit changes?","Save",4)=="Yes":
                    edit.stopEditing(True)
                else:
                    edit.stopEditing(False)
                arcpy.RefreshActiveView()
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)


    def onRectangle(self, rectangle_geometry):
        pass

class matchlandcovButton(object):
    """Implementation for greeninfrastructurev1_addin.matchlandcovButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'matchLandcov')

class parkingFeatureClass(object):
    """Implementation for greeninfrastructurev1_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        save_full = pythonaddins.SaveDialog('Name for parking and roads Layer', "parking")
        save_full = os.path.normpath(save_full)
        save_file = os.path.basename(save_full)
        save_path = save_full.replace(save_file,"")
        mxd = arcpy.mapping.MapDocument('current')
        df = mxd.activeDataFrame
        sr = df.spatialReference
        if sr.name != '':
            if sr.type == 'Projected':
                createdFile = arcpy.CreateFeatureclass_management(save_path,save_file,"POLYGON",spatial_reference=sr)
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

class protectedFeatureClass(object):
    """Implementation for greeninfrastructurev1_addin.protectedFeatureClass (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        save_full = pythonaddins.SaveDialog('Name for Protected Areas Layer', "protected")
        save_full = os.path.normpath(save_full)
        save_file = os.path.basename(save_full)
        save_path = save_full.replace(save_file,"")
        mxd = arcpy.mapping.MapDocument('current')
        df = mxd.activeDataFrame
        sr = df.spatialReference
        if sr.name != '':
            if sr.type == 'Projected':
                createdFile = arcpy.CreateFeatureclass_management(save_path,save_file,"POLYGON",spatial_reference=sr)
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

class squareTool(object):
    """Implementation for greeninfrastructurev1_addin.squareTool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        try:
            layerName = workinglayer.value
        except:
            pythonaddins.MessageBox("Select Working Layer error.","Error",0)
            return None
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        layerds = lyr.dataSource
        dfsr = mxd.activeDataFrame.spatialReference
        if dfsr.name != '':
            if dfsr.type == 'Projected':
                desc = arcpy.Describe(layerds)
                layerSR = desc.spatialReference
                code = layerSR.linearUnitCode
                factor = 1.0
                if code == 9003 or code == 9002:
                    factor = 1.0
                elif code ==9001:
                    factor = 0.3048
                print factor
                print layerSR.name
                pnt = arcpy.Point(x,y)

                pntGeo = arcpy.PointGeometry(pnt, mxd.activeDataFrame.spatialReference)

                print mxd.activeDataFrame.spatialReference.name

                pntLayer = pntGeo.projectAs(layerSR)

                length = math.sqrt(float(comboArea.value)) * factor
                halfLength = float(length)/2.0
                polygonArray = arcpy.Array()
                llX = pntLayer.centroid.X - halfLength
                llY = pntLayer.centroid.Y - halfLength
                polygonArray.add(arcpy.Point(llX,llY))
                ulX = pntLayer.centroid.X - halfLength
                ulY = pntLayer.centroid.Y + halfLength
                polygonArray.add(arcpy.Point(ulX,ulY))
                urX = pntLayer.centroid.X + halfLength
                urY = pntLayer.centroid.Y + halfLength
                polygonArray.add(arcpy.Point(urX,urY))
                lrX = pntLayer.centroid.X + halfLength
                lrY = pntLayer.centroid.Y - halfLength
                polygonArray.add(arcpy.Point(lrX,lrY))
                polygonArray.add(arcpy.Point(llX,llY))
                ws = lyr.workspacePath
                edit = arcpy.da.Editor(ws)
                edit.startEditing(True,False)
                edit.startOperation()
                with arcpy.da.InsertCursor(layerds,['SHAPE@']) as ic:
                    ic.insertRow([arcpy.Polygon(polygonArray,layerSR)])

                arcpy.RefreshActiveView()

                if pythonaddins.MessageBox("Commit changes?","Save",4)=="Yes":
                    edit.stopEditing(True)
                else:
                    edit.stopEditing(False)
                arcpy.RefreshActiveView()
            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

        self.deactivate()

    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass

class rectangleTool(object):
    """Implementation for greeninfrastructurev1_addin.squareTool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        try:
            layerName = workinglayer.value
        except:
            pythonaddins.MessageBox("Select Working Layer error.","Error",0)
            return None
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        layerds = lyr.dataSource
        dfsr = mxd.activeDataFrame.spatialReference
        if dfsr.name != '':
            if dfsr.type == 'Projected':
                desc = arcpy.Describe(layerds)
                layerSR = desc.spatialReference
                code = layerSR.linearUnitCode
                factor = 1.0
                if code == 9003 or code == 9002:
                    factor = 1.0
                elif code ==9001:
                    factor = 0.3048
                print factor
                print layerSR.name
                pnt = arcpy.Point(x,y)
                pntGeo = arcpy.PointGeometry(pnt, mxd.activeDataFrame.spatialReference)

                print mxd.activeDataFrame.spatialReference.name

                pntLayer = pntGeo.projectAs(layerSR)


                halfLength = float(comboWidth.value)/2.0*factor
                halfHeight = float(comboHeight.value)/2.0*factor
                polygonArray = arcpy.Array()
                llX = pntLayer.centroid.X - halfLength
                llY = pntLayer.centroid.Y - halfHeight
                polygonArray.add(arcpy.Point(llX,llY))
                ulX = pntLayer.centroid.X - halfLength
                ulY = pntLayer.centroid.Y + halfHeight
                polygonArray.add(arcpy.Point(ulX,ulY))
                urX = pntLayer.centroid.X + halfLength
                urY = pntLayer.centroid.Y + halfHeight
                polygonArray.add(arcpy.Point(urX,urY))
                lrX = pntLayer.centroid.X + halfLength
                lrY = pntLayer.centroid.Y - halfHeight
                polygonArray.add(arcpy.Point(lrX,lrY))
                polygonArray.add(arcpy.Point(llX,llY))
                ws = lyr.workspacePath
                edit = arcpy.da.Editor(ws)
                edit.startEditing(True,False)
                edit.startOperation()
                with arcpy.da.InsertCursor(layerds,['SHAPE@']) as ic:
                    ic.insertRow([arcpy.Polygon(polygonArray,layerSR)])

                arcpy.RefreshActiveView()

                if pythonaddins.MessageBox("Commit changes?","Save",4)=="Yes":
                    edit.stopEditing(True)
                else:
                    edit.stopEditing(False)

            else:
                pythonaddins.MessageBox('Need a projected coordinate system for the active data frame...', 'Coordinate System', 0)
        else:
            pythonaddins.MessageBox('No Coordinate System defined for the active data frame...', 'Coordinate System', 0)

    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass

class mergePolygons(object):
    """Implementation for greeninfrastructurev1_addin.mergePolygons (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        try:
            layerName = workinglayer.value
        except:
            pythonaddins.MessageBox("Select Working Layer error.","Error",0)
            return None
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        ds = lyr.dataSource
        lyrCount = int(arcpy.GetCount_management(lyr)[0])
        dsCount = int(arcpy.GetCount_management(ds)[0])
        print "Selected: %s out of %s"%(lyrCount,dsCount)
        if lyrCount == dsCount:
            if pythonaddins.MessageBox("Merge all features? Otherwise select the features to merge.",'Selection',4)=="No":
                return None
        if lyrCount > dsCount:
            print "selected count exceeds dataset count"
            return None

        pointList = []
        i = 1
        with arcpy.da.SearchCursor(lyr,["SHAPE@"]) as sc:
            for row in sc:
                print "selected"
                print i
                for part in row[0]:
                    for pnt in part:
                        if not self.checkDuplicates(pnt,pointList):
                            pointList.append(pnt)
                i+=1
        print"Point List length = %s"%(len(pointList))
        if len(pointList) <= 3:
            pythonaddins.MessageBox('There are too few points to merge the polygons...', 'Error', 0)
        else:
            conc = concaveHullSimple()
            k = max(int(math.floor(len(pointList)/4)),3)

            hullPoly = conc.createPolygon(pointList,k)
            if hullPoly != None:
                ws = lyr.workspacePath
                edit = arcpy.da.Editor(ws)
                edit.startEditing(True,False)
                edit.startOperation()
                with arcpy.da.UpdateCursor(lyr,"*") as uc:
                    for row in uc:
                        uc.deleteRow()

                with arcpy.da.InsertCursor(lyr,["SHAPE@"]) as ic:
                    ic.insertRow([hullPoly])
                edit.stopOperation()
                arcpy.RefreshActiveView()
                if pythonaddins.MessageBox("Save edits?","Save",4)=="Yes":
                    edit.stopEditing(True)
                else:
                    edit.stopEditing(False)

            else:
                pythonaddins.MessageBox('Unable to merge selected polygons...', 'Error', 0)
        arcpy.RefreshActiveView()

    def checkDuplicates(self,pnt,lst):
        for chk in lst:
            if pnt.equals(chk):
                return True
        return False

class deletePolygons(object):
    """Implementation for greeninfrastructurev1_addin.mergePolygons (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        layerName = workinglayer.value
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr = arcpy.mapping.ListLayers(mxd,layerName)[0]
        ds = lyr.dataSource
        lyrCount = int(arcpy.GetCount_management(lyr)[0])
        dsCount = int(arcpy.GetCount_management(ds)[0])
        if lyrCount == dsCount:
            if pythonaddins.MessageBox("Delete all features? Otherwise select the features to delete.",'Selection',4)=="No":
                return None
        if lyrCount > dsCount:
            return None
        ws = lyr.workspacePath
        edit = arcpy.da.Editor(ws)
        edit.startEditing(True,False)
        edit.startOperation()
        with arcpy.da.UpdateCursor(lyr,"*") as uc:
            for row in uc:
                uc.deleteRow()
        arcpy.RefreshActiveView()
        if pythonaddins.MessageBox("Save deletion?","Save",4)=="Yes":
            edit.stopEditing(True)
        else:
            edit.stopEditing(False)


class openBMP(object):
    """Implementation for greeninfrastructurev1_addin.mergePolygons (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    # def onClick(self):
    #     fullPath = os.getcwd()
    #     projectName = ""
    #     onlyfiles = [f for f in listdir(fullPath) if isfile(join(fullPath, f))]
    #     excelFiles = [f for f in onlyfiles if f.endswith("xlsm")]
    #     projectFiles = [f for f in onlyfiles if f.endswith("mxd")]
    #     #print excelFiles
    #
    #     if len(projectFiles) < 1:
    #         pythonaddins.MessageBox("After loading the toolbar, Please create, open or reopen the project","Open BMP",0)
    #     else:
    #         #pythonaddins.MessageBox((fullPath + "\\" + projectName),"Open BMP",0)
    #         if len(excelFiles) < 1:
    #             pythonaddins.MessageBox("After loading the toolbar, Please create, open or reopen the project","Open BMP",0)
    #         else:
    #             for projectName  in excelFiles:
    #                 excelFile = fullPath + "\\" + projectName
    #                 Popen(excelFile, shell=True)
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'LoadProjectExcel')

class pdfReport(object):
    """Implementation for greeninfrastructurev1_addin.mergePolygons (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    # def onClick(self):
    #     fullPath = os.getcwd()
    #     projectName = ""
    #     onlyfiles = [f for f in listdir(fullPath) if isfile(join(fullPath, f))]
    #     excelFiles = [f for f in onlyfiles if f.endswith("xlsm")]
    #     projectFiles = [f for f in onlyfiles if f.endswith("mxd")]
    #     #print excelFiles
    #
    #     if len(projectFiles) < 1:
    #         pythonaddins.MessageBox("After loading the toolbar, Please create, open or reopen the project","Open BMP",0)
    #     else:
    #         #pythonaddins.MessageBox((fullPath + "\\" + projectName),"Open BMP",0)
    #         if len(excelFiles) < 1:
    #             pythonaddins.MessageBox("After loading the toolbar, Please create, open or reopen the project","Open BMP",0)
    #         else:
    #             for projectName  in excelFiles:
    #                 excelFile = fullPath + "\\" + projectName
    #                 Popen(excelFile, shell=True)
    def onClick(self):
        current = os.path.dirname(os.path.realpath(__file__))
        fname = current + "\\greeninfview.pyt"
        if os.path.isfile(fname):
            pythonaddins.GPToolDialog(fname, 'CreatePDFMap')

class concaveHullSimple(object):
    #See:
    def __init__(self):
        self.pointList = []
        self.k = 30


    def createPolygon(self,points, k=3):#polygonList):
        print "Current k %s"%k
        self.pointList = []
        dataset = []
        #for poly in polygonList:
            #for part in poly:
                #for pnt in part:
                    #if pnt not in self.pointList:
                        #self.pointList.append(pnt)
                        #dataset.append(pnt)
        for pnt in points:
            self.pointList.append(pnt)
            dataset.append(pnt)

        print len(self.pointList)

        if len(self.pointList)<3:
            return None
        if k>len(self.pointList):
            return None


        firstPoint = self.findMinYPoint(self.pointList)
        print firstPoint

        hull = arcpy.Array()
        hull.append(firstPoint)
        currentPoint = firstPoint
        self.pointList.remove(firstPoint)
        previousPoint = firstPoint
        step = 2
        cutoff = math.floor(float(len(self.pointList))/2)

        print "Number k: %s"%(k)
        while ((currentPoint != firstPoint) or (step==2)) and (len(self.pointList)>0):
            if step >1000000:
                print "loop kept going"
                return None
            print "Step %s" %(step)

            if step == 5:
                self.pointList.append(firstPoint)
            kNearestPoints = self.getNearestNeighbors(self.pointList,currentPoint,k)


            cpoints = self.sortByAngle(kNearestPoints,currentPoint,previousPoint)
            #print len(cpoints)
            cpoint = None
            its = True
            if hull.count >= 2:
                for cpoint in cpoints:
                    newEdge = arcpy.Polyline(arcpy.Array([currentPoint,cpoint]))
                    startHull = 0
                    if firstPoint.equals(cpoint):
                        print "cpoint equals firstpoint, length of pointList %s"%len(self.pointList)
                        startHull +=1
                    crosses = False
                    for i in range(startHull,hull.count,1):
                        #try:
                        if i == hull.count-1:
                            #print "last check"
                            tempLine =arcpy.Polyline(arcpy.Array([hull[i],hull[0]]))
                            crosses = newEdge.crosses(tempLine)
                            #print "Crosses back %s"%crosses
                            break
                        tempLine =arcpy.Polyline(arcpy.Array([hull[i],hull[i+1]]))
                        crosses = newEdge.crosses(tempLine)
                        #print "Crosses %s"%(crosses)
                        if crosses == True:
                            break
                            #if cpoint.disjoint(tempLine) == True:
                                #print "Not on Edge"
                            #else:
                                #print "On Edge"
                        #except:
                            #print "error in crosses check"

                    if crosses == False:
                        its = False
                        break

            else:
                its = False
                cpoint = cpoints[0]
            if its == True:
                print "Intersects, probably should increase k"
                newk=k+1
                poly = self.createPolygon(points,newk)
                return poly
            previousPoint = currentPoint
            currentPoint = cpoint
            hull.append(cpoint)
            #for i in range(0,hull.count):
                #print "%s,%s"%(hull[i].X,hull[i].Y)
            self.pointList.remove(currentPoint)
            step+=1
        #hull.append(firstPoint)
        hullPolygon = arcpy.Polygon(hull)
        print "Part count %s" % hullPolygon.partCount
        if hullPolygon.partCount > 1:
            print "Not all points contained increasing k"
            newk=k+1
            if newk > len(points)-1:
                return None
            poly = self.createPolygon(points,newk)
            return poly
        contains = True
        #within = True
        #touches = True
        disj = False
        for pnt in dataset:
            contains = hullPolygon.contains(pnt)
            #within = pnt.within(hullPolygon)
            #touches = hullPolygon.touches(pnt)
            disj = hullPolygon.disjoint(pnt)
            #print contains
            if disj==True:
                print "Not all points contained increasing k"
                newk=k+1
                if newk > len(points)-1:
                    print "Exceeds the number of points"
                    return hullPolygon
                poly = self.createPolygon(points,newk)
                return poly

        return hullPolygon


    def findMinYPoint(self, pointList):
        minY = 10000000**10
        minPnt = arcpy.Point(0,0)
        for pnt in pointList:
            if pnt.Y < minY:
                minY = pnt.Y
                minPnt = pnt
        return minPnt

    def findMinlrPoint(self, pointList):
        minY = 10000000**10
        maxX = -(10000000**10)
        minPnt = arcpy.Point(0,0)
        for pnt in pointList:
            if pnt.Y <= minY and pnt.X >= maxX:
                minY = pnt.Y
                maxX = pnt.X
                minPnt = pnt
        return minPnt

    def getNearestNeighbors(self, pointList, point, k):
        distanceList = []
        for i, pnt in enumerate(pointList):
            distanceList.append((self.distance(point,pnt),i))
        distanceList.sort()
        nearest = []
        endLst = min(len(distanceList),k)
        for x in range(0,endLst):
            indx = distanceList[x][1]
            nearest.append(pointList[indx])
        return nearest


    def distance(self,point1,point2):
        dx = point1.X - point2.X
        dy = point1.Y - point2.Y
        return math.sqrt(dx*dx+dy*dy)

    def sortByAngle(self,nearest,point,prevPoint):
        angles = []
        for indx,nearestPoint in enumerate(nearest):
            angle1 = math.atan2(prevPoint.Y - point.Y,prevPoint.X-point.X)
            angle2 = math.atan2(nearestPoint.Y - point.Y,nearestPoint.X-point.X)
            angleDiff = (180.0 / math.pi * (angle2-angle1))
            angles.append((angleDiff%360,indx))
            #if angleDiff>0:
                #angles.append((360-angleDiff,indx))
            #else:
                #angles.append((-angleDiff,indx))
        angles.sort(reverse=True)
        sortedNearest = []
        for angle, indx in angles:
            sortedNearest.append(nearest[indx])
        return sortedNearest









