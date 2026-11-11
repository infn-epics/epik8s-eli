from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory

import os
from java.lang import Exception

def csv_to_list(csv_file):
    result = []

    with open(csv_file, 'r') as file:
        # Read lines from the file
        lines = file.readlines()
        # Extract the header
        header = [col.strip() for col in lines[0].split(",")]
        # Process each row
        for line in lines[1:]:
            values = [value.strip() for value in line.split(",")]
            row_dict = dict(zip(header, values))
            result.append(row_dict)
    return result

logger = ScriptUtil.getLogger()

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
zoneSelector = widget.getEffectiveMacros().getValue("ZONE")
typeSelector = widget.getEffectiveMacros().getValue("TYPE")
wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template
display_model = widget.getDisplayModel()

display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))
confpath = display_path + "/" + conffile

if not os.path.exists(confpath):
    ScriptUtil.showMessageDialog(widget, "Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")

if zoneSelector == None:
    zoneSelector = PVUtil.getString(ScriptUtil.getPVs(widget)[0])

if typeSelector == None:
    typeSelector = PVUtil.getString(ScriptUtil.getPVs(widget)[1])
    


# Parse conf file
print("LOADING:" + confpath + " zoneSelector: \"" + zoneSelector + " typeSelector: \"" + str(typeSelector)+"\"")

devinfo = csv_to_list(confpath)

# Initialize an empty list to store the values
devices = []
device_prefix = widget.getEffectiveMacros().getValue("P")

# Process each device
for device in devinfo:
    # logger.info("device " + device['Name'] + " zone " + device['Zone'] + " type " + device['Type'])
    opi="moto-ele.bob"
    if zoneSelector and zoneSelector != "ALL" and zoneSelector != device['Zone']:
        continue
    if typeSelector and typeSelector != "ALL" and typeSelector != device['Type']:
        continue
    if "Opi" in device:
        opi=device['Opi']
    devices.append({'R': device['Name'], "P": device_prefix, "TYPE": device['Type'], "ZONE": device['Zone'],"OPI":opi})
    logger.info("loading " + device['Name'])

off=5
embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height")+off

def createInstance(x, y, macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget();
    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
            embedded.getPropertyValue("macros").add(macro, value)
    embedded.setPropertyValue("file", macros['OPI'])
    return embedded

rows = 35
for i in range(len(devices)):
    # x = (i / rows) * embedded_width
    # y = 170 + embedded_height*(i % rows)
    x=0
    y= i * embedded_height
    instance = createInstance(x, y, devices[i],)
    widget.runtimeChildren().addChild(instance)