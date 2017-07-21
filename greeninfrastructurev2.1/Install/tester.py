import cPickle as pickle
from g2gproject import Project
import arcpy
arcpy.env.overwriteOutput = True
arcpy.ImportToolbox(r"C:\Users\davidlamb\Documents\GitHub\greytogreen\greeninfrastructurev2.1\Install\greeninfview.pyt")
import os
arcpy.CheckOutExtension("3D")
#i = 1
for file in os.listdir(r"C:\Users\davidlamb\Downloads\update20170712"):
        if file.endswith(".p"):
            pth = os.path.join(r"C:\Users\davidlamb\Downloads\update20170712",file)
            print pth
            #if i >3:
#pth=r"C:\Users\davidlamb\Downloads\update20170712\debugprotectedarea_none.p"
            arcpy.CalculateAreas_greeninfview(pth)
#pth=r"C:\Users\davidlamb\Downloads\update20170712\debugProtectedArea.p"
#arcpy.CalculateAreas_greeninfview(pth)

            _project = pickle.load(open(pth,'rb'))
            _project.outputPDFMap()
            _project.exportNewToKML()
            #i+=1

#_project.interDissExclude([r"C:\Users\davidlamb\Downloads\update20170712\gt_full.gdb\building10to50"],[r"C:\Users\davidlamb\Downloads\update20170712\gt_full.gdb\allImpervious_diss"],"c_rr_treesmanual")
#_project.imperviousPerviousAreas()
