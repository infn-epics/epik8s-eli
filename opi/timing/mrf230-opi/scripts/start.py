from org.csstudio.opibuilder.scriptUtil import FileUtil, ConsoleUtil, ScriptUtil
from java.lang import Runtime, Process, String
from jarray import array
import time 
from org.eclipse.jface.dialogs import MessageDialog

### Run external Python script that does the CA puts and start.
### Write currently loaded configuration to GUI (or 'Error'). 

ConsoleUtil.writeInfo("Executing script start.py")

wait = 5000

configfile = display.getWidget("Choose_path").getValue()

file_name = "loadedFile.txt"
file_dir = widget.getMacroValue("loadedPath")
file_path = file_dir + file_name

evr_name = "evrList.txt"
evr_dir = widget.getMacroValue("confPath")
evr_path = evr_dir + evr_name

log_name = "start_" + time.strftime("%d%m%Y") + time.strftime("%H%M%S") + ".log"
log_dir = widget.getMacroValue("logPath")
log_path = log_dir + log_name

prog_name = "extStart.py"

opi_path = display.getModel().getOpiFilePath()
try:
     abs_path = FileUtil.workspacePathToSysPath(str(opi_path))
except:
     # opi_path most likely already contains absolute path
     abs_path = str(opi_path)	
dir_path = abs_path[:abs_path.rfind("/")] + "/scripts/"

cmdarr = array(["gnome-terminal", "--disable-factory", "--execute", "/bin/bash", "-c", "%s%s %s %s %s %s 2>&1 | tee %s && sleep 10" %(dir_path, prog_name, configfile, file_path, evr_path, log_path, log_path)], String) 

ConsoleUtil.writeInfo("CMD: " + repr(cmdarr))

runtime = Runtime.getRuntime()

# Run external program 
p = runtime.exec(cmdarr)

# Wait for external process to finish
p.waitFor()

# Write info about loaded configuration to text widget in GUI
try:
	loaded = FileUtil.readTextFile(str(file_path))
	display.getWidget("Loaded_file").setValue(str(loaded).rstrip())
	display.getWidget("Star_main").setValue(' ')
except:
	pass

# Manage indicators of save status
pv = display.getWidget("Saved").getPV()
pv.setValue(1)
