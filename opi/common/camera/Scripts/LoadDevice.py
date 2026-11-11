from org.csstudio.display.builder.runtime.script import ScriptUtil,PVUtil
#from org.csstudio.display.builder.runtime import ActionUtil
import os
from java.lang import Exception
logger = ScriptUtil.getLogger()


conffile = widget.getEffectiveMacros().getValue("CONFFILE")
display_model =  widget.getDisplayModel()


logger.info("LOAD Devices, Device file "+conffile + " PV: "+str(pvs[0]))
display_path = display_model.getUserData(display_model.USER_DATA_INPUT_FILE)
#percorso_assoluto = os.path.abspath(".")
#logger.info("LOAD Devices, percorso assoluto " + percorso_assoluto)

directory = os.path.dirname(display_path) +"/../../ini/" 

#logger.info("LOAD Devices, $PWD " + display_model )
if not os.path.exists(conffile):
    opihome=os.getenv("OPIHOME",".")
    ini=opihome+"/ini"
    conffile_try=ini+"/"+conffile
    if not os.path.exists(conffile_try):
        conffile=directory + conffile
    else:
        conffile=conffile_try


if not os.path.exists(conffile):
    ScriptUtil.showMessageDialog(widget,"Cannot find  file \""+conffile+"\" please set CONFILE macro to a correct file")

    
motorf = os.path.abspath(conffile)

logger.info("LOAD opening "+conffile )
combo = ScriptUtil.findWidgetByName(widget, "DeviceCombo")
# axis = ScriptUtil.findWidgetByName(widget, "TML_AXIS")

# Initialize an empty list to store the values
device_list = []

# Open the file and read values into the list
with open(motorf, 'r') as file:
    for line in file:
        # Strip whitespace characters (like newline) from each line
        stripped_line = line.strip()
        if stripped_line:  # Avoid adding empty lines
            logger.info("loading " +stripped_line )
            device_list.append(stripped_line)


combo.setItems(device_list)

if len(device_list): ## put the first as default
    ScriptUtil.getPrimaryPV(combo).write(device_list[0])


