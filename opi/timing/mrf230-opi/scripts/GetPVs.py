from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, ScriptUtil, ConsoleUtil, GUIUtil
from org.eclipse.jface.dialogs import MessageDialog
from java.lang import Runtime, Process, String
from jarray import array
import time

### Run external Python script that does the CA gets and stores the values in a json file.

ConsoleUtil.writeInfo("Executing script GetPVs.py")

wait = 5000

def check_file_exists(path):
	try:
		s = open(path, 'r')
		s.close()
	except Exception:
		return False
		
	return True

opi_path = display.getModel().getOpiFilePath()
try:
     abs_path = FileUtil.workspacePathToSysPath(str(opi_path))
except:
     # opi_path most likely already contains absolute path
     abs_path = str(opi_path)	
dir_path = abs_path[:abs_path.rfind("/")] + "/scripts/"

configfile = display.getWidget("Choose_path").getValue()

file_name = "loadedFile.txt"
file_dir = widget.getMacroValue("loadedPath")
file_path = file_dir + file_name

evr_name = "evrList.txt"
evr_dir = widget.getMacroValue("confPath")
evr_path = evr_dir + evr_name

log_name = "save_" + time.strftime("%d%m%Y") + time.strftime("%H%M%S") + ".log"
log_dir = widget.getMacroValue("logPath")
log_path = log_dir + log_name

prog_name = "extGetPVs.py"

cmdarr = array(["gnome-terminal", "--disable-factory", "--execute", "/bin/bash", "-c", "%s%s %s %s %s %s 2>&1 | tee %s && sleep 10" %(dir_path, prog_name, configfile, file_path, evr_path, log_path, log_path)], String) 

runtime = Runtime.getRuntime()

def main():
	if display.getWidget("Loaded_file").getValue() == 'Stopped':
		prompt = GUIUtil.openConfirmDialog("No configuration running. Save anyway?")
		if (not prompt):
			return False
	elif not configfile:
		MessageDialog.openWarning(None, "Warning", "No configuration file name. Please enter name.")
		return False
	elif not configfile.endswith(".json"):
		MessageDialog.openWarning(None, "Warning", "Configuration file needs extension '.json'.")
		return False
	elif (check_file_exists(configfile) == True):
		prompt = GUIUtil.openConfirmDialog("Overwrite file?\n" + configfile)
		if (not prompt):
			return False
	
	p = runtime.exec(cmdarr)
	p.waitFor()
	loaded = FileUtil.readTextFile(str(file_path))
	display.getWidget("Loaded_file").setValue(str(loaded).rstrip())
	display.getWidget("Star_main").setValue(' ')

main()

pv = display.getWidget("Saved").getPV()
pv.setValue(1)
