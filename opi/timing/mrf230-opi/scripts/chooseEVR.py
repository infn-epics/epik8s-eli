from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil

logger = ScriptUtil.getLogger()
pv = PVUtil.getString(pvs[0])
# var pv = PVUtil.getString(pvs[0]);
# var ms=widget.getPropertyValue("macros")

# ms.getNames().forEach(element => {
#     logger.info("MACRO name ="+element +" value="+ms.getValue(element))

# });
# var device_macro = ms.getValue("EVR");
logger.info("PV Name " + str(pvs[0]) + " Val:"+pv)

widget.getPropertyValue("macros").add("EVR", pv)
widget.setPropertyValue("file","")
widget.setPropertyValue("file","Timing_EVR_Main.bob")


