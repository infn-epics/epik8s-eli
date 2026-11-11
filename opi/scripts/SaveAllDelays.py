from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil

P = widget.getEffectiveMacros().getValue("P") or "LEL:TIM"
EVRS = ["EVR-BPMCAM", "EVR-CAM", "EVR-ADC", "EVR-LAS", "EVR-LLRF", "EVR-RFD", "EVR-RFM"]

filename = ScriptUtil.showSaveAsDialog(widget, "timing_delays.csv")
if filename is not None:
    if not filename.endswith(".csv"):
        filename += ".csv"

    rows = []
    errors = []

    for R in EVRS:
        for N in range(4):
            base = P + ":" + R + ":Pul" + str(N) + "-"
            for suffix in ["Delay-SP", "Width-SP", "Evt-Trig0-SP", "Label-I"]:
                pvname = base + suffix
                try:
                    pv = PVUtil.createPV(pvname, 1000)
                    if "Label" in pvname:
                        value = PVUtil.getString(pv)
                    else:
                        value = str(PVUtil.getDouble(pv))
                    rows.append(pvname + "," + value)
                except Exception as e:
                    errors.append(pvname + ": " + str(e))

    with open(filename, "w") as f:
        f.write("\n".join(rows) + "\n")

    msg = "Saved " + str(len(rows)) + " values (" + str(len(EVRS)) + " EVRs x 4 channels) to:\n" + filename
    if errors:
        msg += "\n\nErrors (" + str(len(errors)) + "):\n" + "\n".join(errors[:10])
    ScriptUtil.showMessageDialog(widget, msg)
