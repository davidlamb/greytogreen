import cPickle as pickle
from g2gproject import Project
import arcpy
arcpy.env.overwriteOutput = True
_project = pickle.load(open(r"C:\Users\davidlamb\Downloads\update20170712\debugProtectedArea.p",'rb'))
#_project.interDissExclude([r"C:\Users\davidlamb\Downloads\update20170712\gt_full.gdb\building10to50"],[r"C:\Users\davidlamb\Downloads\update20170712\gt_full.gdb\allImpervious_diss"],"c_rr_treesmanual")
_project.imperviousPerviousAreas()