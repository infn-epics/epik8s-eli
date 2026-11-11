from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil

logger = ScriptUtil.getLogger()
pv = PVUtil.getLong(pvs[0])
logger.info("PV Name " + str(pvs[0]) + " Val:"+str(pv))
widget.getPropertyValue("macros").add("FP", str(pv))
widget.setPropertyValue("file","")
widget.setPropertyValue("file","Timing_Output.bob")
