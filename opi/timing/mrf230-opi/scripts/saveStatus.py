from org.csstudio.opibuilder.scriptUtil import FileUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil
from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil


# Display whether current configuration is saved
# Need this for first execution and for save actions from main screen
# Any direct changes to PVs w/o saving are taken care of by other script

opi_path = ScriptUtil.workspacePathToSysPath(widget.getDisplayModel().getUserData("_input_file"))
ConsoleUtil.writeInfo("Executing script saveStatus.py opi:"+opi_path + " pvs[0]:"+PVUtil.getString(pvs[0]))

## opi_path = display.getModel().getOpiFilePath()
try:
     abs_path = FileUtil.workspacePathToSysPath(str(opi_path))
except:
     # opi_path most likely already contains absolute path
     abs_path = str(opi_path)	
dir_path = abs_path[:abs_path.rfind("/")] + "/scripts/"
file_name = "loadedFile.txt"
file_dir = PVUtil.getString(pvs[2])
file_path = file_dir + file_name
		
try:
	loaded = FileUtil.readTextFile(str(file_path))

	if (triggerPV == pvs[0]):
		if str(loaded).endswith('*\n'):
			display.getWidget("Star").setValue('*')
	elif (triggerPV == pvs[1]):
		display.getWidget("Star").setValue(' ')
	
except:
    ScriptUtil.showMessageDialog(widget,"["+PVUtil.getString(pvs[0])+"] There is no information on the loaded configuration. Looking for "+str(file_path))
