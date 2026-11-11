from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.model.properties import WidgetColor
import time

# 1. Configuration
SECTION_PUMPS = [
    "LEL:VAC:VPCON01:IONP01:PRES",
    "LEL:VAC:VPCON01:IONP02:PRES",
    "LEL:VAC:VPCON01:IONP03:PRES",
    "LEL:VAC:VPCON01:IONP04:PRES",
    "LEL:VAC:VGCON01:CC01:PRES",
    "LEL:VAC:VGCON01:CC03:PRES",
    "LEL:VAC:VGCON01:CC04:PRES"
]

TIMEOUT_THRESHOLD = 10.0 # Seconds

# 2. Colors
RED    = WidgetColor(255, 0, 0)
ORANGE = WidgetColor(255, 165, 0)
GREEN  = WidgetColor(0, 255, 0)
PURPLE = WidgetColor(255, 0, 255)

# Use the widget's persistent internal storage
# We initialize it if it doesn't exist yet
if not "first_lost_time" in globals():
    first_lost_time = None

try:
    highest_severity = 0
    found_any = False
    connection_lost = False

    for pv in pvs:
        name_part = pv.getName().split("://")[-1].split(".")[0].strip()
        
        if name_part in SECTION_PUMPS:
            found_any = True
            sev = PVUtil.getSeverity(pv)
            
            # Severity 3 = INVALID (Disconnected)
            if sev >= 3:
                connection_lost = True
            
            if sev > highest_severity:
                highest_severity = sev

    now = time.time()

    if connection_lost:
        # If we just started losing connection, mark the time
        if first_lost_time is None:
            first_lost_time = now
        
        elapsed = now - first_lost_time
        
        if elapsed < TIMEOUT_THRESHOLD:
            # Within 10s: Show Orange to avoid "Panic Red"
            target_color = ORANGE
        else:
            # After 10s: Confirm as Red alarm
            target_color = RED
    else:
        # Connection is fine: Reset the timer and use standard alarm logic
        first_lost_time = None
        if highest_severity == 0:
            target_color = GREEN
        elif highest_severity == 1:
            target_color = ORANGE
        else:
            target_color = RED

    # Apply Color
    if not found_any:
        widget.setPropertyValue('background_color', PURPLE)
    else:
        widget.setPropertyValue('background_color', target_color)

except Exception as e:
    print("M1 Script Error: " + str(e))
    widget.setPropertyValue('background_color', PURPLE)