from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.opibuilder.scriptUtil import FileUtil
from org.csstudio.opibuilder.scriptUtil import ScriptUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil

from org.eclipse.jface.dialogs import MessageDialog

# Update 
# 1) loadedFile.txt 
# 2) Star on EVR screen
# 3) local PV that directly appends star on loaded status on main screen
# to indicate that the configuration is out of date

ConsoleUtil.writeInfo("Executing script unsavedInfo.py")

display.getWidget("Star").setValue('*')

opi_path = display.getModel().getOpiFilePath()
try:
     abs_path = FileUtil.workspacePathToSysPath(str(opi_path))
except:
     # opi_path most likely already contains absolute path
     abs_path = str(opi_path)	
dir_path = abs_path[:abs_path.rfind("/")] + "/scripts/"
file_name = "loadedFile.txt"
pv_path = display.getWidget("Loaded_Path").getPV()
file_dir = PVUtil.getString(pv_path)
file_path = file_dir + file_name

try:
	loaded = FileUtil.readTextFile(str(file_path))

	if str(loaded).endswith('.json\n'):
		FileUtil.writeTextFile(str(file_path), False, None, '*', True)

except:
	pass

pv = display.getWidget("Unsaved").getPV()
pv.setValue(1)

