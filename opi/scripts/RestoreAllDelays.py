from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from javax.swing import JFileChooser, JOptionPane, JScrollPane, JTextArea
from javax.swing.filechooser import FileNameExtensionFilter

# ── 1. Pick file ───────────────────────────────────────────────────────────────
chooser = JFileChooser()
chooser.setDialogTitle("Select delay snapshot to restore")
chooser.setFileFilter(FileNameExtensionFilter("CSV Snapshot files (*.csv)", ["csv"]))
if chooser.showOpenDialog(None) != JFileChooser.APPROVE_OPTION:
    pass  # cancelled
else:
    filename = chooser.getSelectedFile().getAbsolutePath()

    # ── 2. Parse CSV (pvname,value) ────────────────────────────────────────────
    entries = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                pvname, value = line.split(",", 1)
                entries.append((pvname.strip(), value.strip()))

    if not entries:
        ScriptUtil.showMessageDialog(widget, "No entries found in:\n" + filename)
    else:
        # ── 3. Diff: compare saved vs current (Delay and Width only) ──────────
        diffs = []
        read_errors = []
        for pvname, saved_val in entries:
            if "Label" in pvname:
                continue
            try:
                pv = PVUtil.createPV(pvname, 1000)
                actual = PVUtil.getDouble(pv)
                saved_num = float(saved_val)
                if abs(actual - saved_num) > 1e-9:
                    diffs.append((pvname, saved_num, actual))
            except Exception as e:
                read_errors.append((pvname, saved_val, "ERROR: " + str(e)))

        diffs_all = diffs + read_errors

        # ── 4. Build diff report ───────────────────────────────────────────────
        sep = "-" * 82
        if not diffs_all:
            diff_lines = [
                "No differences found between snapshot and current delays.",
                "Total PVs: " + str(len(entries)),
                "",
                "Do you still want to apply the restore?"
            ]
        else:
            diff_lines = [
                "Differences (" + str(len(diffs_all)) + " of " + str(len(entries)) + " PVs):",
                "",
                "{:<58} {:>10} {:>10}".format("PV", "Saved", "Current"),
                sep
            ]
            for pvname, saved, actual in diffs:
                diff_lines.append("{:<58} {:>10.6g} {:>10.6g}".format(
                    pvname[-57:], saved, actual))
            for pvname, saved, err in read_errors:
                diff_lines.append("{:<58}  {}".format(pvname[-57:], err[:20]))
            diff_lines += [sep, "", "Proceed with restore?"]

        diff_text = "\n".join(diff_lines)
        text_area = JTextArea(diff_text, min(28, len(diff_lines) + 3), 88)
        text_area.setEditable(False)
        text_area.setFont(text_area.getFont().deriveFont(12.0))

        choice = JOptionPane.showConfirmDialog(
            None, JScrollPane(text_area),
            "Restore delays from: " + chooser.getSelectedFile().getName(),
            JOptionPane.YES_NO_OPTION,
            JOptionPane.WARNING_MESSAGE
        )

        if choice != JOptionPane.YES_OPTION:
            pass  # cancelled
        else:
            # ── 5. Apply ───────────────────────────────────────────────────────
            applied = 0
            errors = []
            for pvname, value in entries:
                try:
                    pv = PVUtil.createPV(pvname, 1000)
                    if "Label" in pvname:
                        pv.write(value)
                    else:
                        pv.write(float(value))
                    applied += 1
                except Exception as e:
                    errors.append(pvname + ": " + str(e))

            msg = "Restored " + str(applied) + " of " + str(len(entries)) + " values."
            if errors:
                msg += "\n\nErrors:\n" + "\n".join(errors[:10])
            ScriptUtil.showMessageDialog(widget, msg)
