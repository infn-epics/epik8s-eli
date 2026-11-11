from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil

logger = ScriptUtil.getLogger()
pv = PVUtil.getString(pvs[0])
device_actual = widget.getEffectiveMacros().getValue("DEVICE")
logger.info("SELECTION:"+pv)

if device_actual and pv:
    vals=pv.split()
    newdev=device_actual+vals[0]
    logger.info("PV Name " + str(pvs[0]) + " Val:"+vals[0] +" DEVICE:"+device_actual+ " Model:"+vals[1])
    widget.setPropertyValue("file","")
    widget.getPropertyValue("macros").add("CAM", vals[0])
    widget.getPropertyValue("macros").add("HW", vals[1])
    widget.setPropertyValue("file","Camera_Main.bob")


