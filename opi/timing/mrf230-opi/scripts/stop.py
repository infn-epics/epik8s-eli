from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.opibuilder.scriptUtil import FileUtil
from org.csstudio.opibuilder.scriptUtil import ScriptUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil
from org.csstudio.opibuilder.scriptUtil import GUIUtil

from org.eclipse.jface.dialogs import MessageDialog

# Stop sequence and write info on screen

ConsoleUtil.writeInfo("Executing script stop.py")

file_name = "loadedFile.txt"
file_dir = widget.getMacroValue("loadedPath")
file_path = file_dir + file_name

pv = widget.getPV()
loadsts = PVUtil.getString(display.getWidget('Run_status').getPV())

if loadsts == 'Loaded': 
	prompt = GUIUtil.openConfirmDialog("Do you want to stop the sequence?")
	if prompt:
		FileUtil.writeTextFile(str(file_path), False, 'Stopped', False)
		display.getWidget("Loaded_file").setValue('Stopped')
		pv.setValue(1)
		
elif loadsts == 'Unloaded': 
	 MessageDialog.openWarning(None, "Warning", "The sequence is not running.")



