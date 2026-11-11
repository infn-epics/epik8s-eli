from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil

filename_widget = ScriptUtil.findWidgetByName(widget, "confload")
name = PVUtil.getString(ScriptUtil.getPrimaryPV(filename_widget))

if name:
    print("applying file:" + name)
    with open(name, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split(',', 1)
                dest_pv = PVUtil.createPV(key, 1000)
                if dest_pv:
                    if "Label" in key:
                        dest_pv.write(value)
                    else:
                        dest_pv.write(float(value))
                else:
                    ScriptUtil.showMessageDialog(widget, "error connecting " + key)
    ScriptUtil.showMessageDialog(widget, "Applied settings " + name)
else:
    ScriptUtil.showMessageDialog(widget, "NO configuration loaded")
