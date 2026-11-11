from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil

device_prefix = widget.getEffectiveMacros().getValue("P")
sub_prefix = widget.getEffectiveMacros().getValue("R")
full_prefix = device_prefix + ":" + sub_prefix

name = ScriptUtil.showSaveAsDialog(widget, "")
if name:
    print("selected path:" + name)
    with open(name, 'w') as f:
        for cnt in range(4):
            for suffix in ["Pul" + str(cnt) + "-Delay-SP",
                           "Pul" + str(cnt) + "-Width-SP",
                           "Pul" + str(cnt) + "-Evt-Trig0-SP",
                           "Pul" + str(cnt) + "-Label-I"]:
                pvn = full_prefix + ":" + suffix
                pv = PVUtil.createPV(pvn, 1000)
                if "Label" in pvn:
                    value = PVUtil.getString(pv)
                else:
                    value = PVUtil.getDouble(pv)
                f.write(pvn + "," + str(value) + "\n")
    ScriptUtil.showMessageDialog(widget, "written " + name)
