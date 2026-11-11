from org.csstudio.opibuilder.scriptUtil import ConsoleUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, DataUtil


ConsoleUtil.writeInfo("Executing script runningUnsaved.py")

# w=ScriptUtil.findWidgetByName(widget, "Loaded_file")

# saved= w.getValue()
# saved = display.getWidget("Loaded_file").getValue()
saved = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Loaded_file")))

new = saved + '*'

if saved.endswith('.json'):
	# w.setValue(str(new))
 	ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Loaded_file")).setValue(str(new))

# ScriptUtil.findWidgetByName(widget,"Star_main").setValue('*')
ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Star_main")).setValue('*')