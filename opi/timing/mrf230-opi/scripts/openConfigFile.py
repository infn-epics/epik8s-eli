from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.opibuilder.scriptUtil import FileUtil
from org.csstudio.opibuilder.scriptUtil import ScriptUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil

from org.eclipse.jface.dialogs import MessageDialog

### Open the selected configuration file with gedit

ConsoleUtil.writeInfo("Executing script openConfigFile.py")

wait = 5000

file_name = display.getWidget("Choose_path").getValue()
cmd = "gedit " + file_name

if not file_name:
		MessageDialog.openWarning(None, "Warning", "No configuration file selected. Please select a file.")
elif not file_name.endswith(".json"):
	MessageDialog.openWarning(None, "Warning", "No json configuration file selected. Please select a json file.")
else:
	ConsoleUtil.writeInfo("Opening file " + str(file_name))
	ScriptUtil.executeSystemCommand(cmd, wait)

