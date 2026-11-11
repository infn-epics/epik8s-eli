from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
# Jython: 'except Exception' does NOT catch Java exceptions (createPV throws
# java.lang.Exception on timeout), so catch Throwable explicitly.
from java.lang import Throwable

# Switch the embedded CompactCamera panel to the camera picked in CamMenu.
# The switch must never depend on a PV connecting quickly: over the VPN or
# through the gateway the first CA search can take more than a second, and a
# createPV timeout used to abort the script after stopping the old camera but
# before loading the new one (combo showing camera B, panel still on A).

StopPrevAcq = True
TIMEOUT_MS = 3000


def read_string(name):
    """Read a PV as string, or return None if it doesn't connect in time."""
    pv = None
    try:
        pv = PVUtil.createPV(name, TIMEOUT_MS)
        return PVUtil.getString(pv)
    except (Exception, Throwable) as e:
        print("reloadpanel: cannot read %s: %s" % (name, e))
        return None
    finally:
        if pv is not None:
            PVUtil.releasePV(pv)


def stop_acquisition(name):
    pv = None
    try:
        pv = PVUtil.createPV(name, TIMEOUT_MS)
        pv.write(0)
        print("Stopped acquisition: " + name)
    except (Exception, Throwable) as e:
        print("reloadpanel: cannot stop %s: %s" % (name, e))
    finally:
        if pv is not None:
            PVUtil.releasePV(pv)


sel = PVUtil.getString(pvs[0])
print("User selection: " + sel)

vals = sel.split(" (")
if len(vals) > 1:  # "NULL" (combo initialisation) has no "(ioc)" part
    cam_name = vals[0]
    mydev = widget.getEffectiveMacros().getValue("DEVICE")
    old_cam = widget.getEffectiveMacros().getValue("CAM")

    if cam_name != old_cam:
        # Model label only: never let it block the switch. If the IOC doesn't
        # answer, skip the second read so a dead camera costs one timeout.
        cam_model = ""
        man = read_string("pva://" + mydev + ":" + cam_name + ":Manufacturer_RBV")
        if man is not None:
            mod = read_string("pva://" + mydev + ":" + cam_name + ":Model_RBV")
            if mod is not None:
                cam_model = man + "-" + mod
        print("Camera: " + cam_name + " Model: " + cam_model)

        # Trick to reload the embedded panel with the new macros.
        widget.setPropertyValue("file", "")
        macros = widget.getPropertyValue("macros")
        macros.add("CAM", cam_name)
        macros.add("HW", cam_model)
        widget.setPropertyValue("file", "CompactCamera.bob")

        # Stop the previous camera only after the new one is loaded.
        if StopPrevAcq and old_cam:
            stop_acquisition("pva://" + mydev + ":" + old_cam + ":Acquire")
