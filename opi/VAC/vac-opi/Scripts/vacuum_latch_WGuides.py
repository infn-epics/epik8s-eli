from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.model.properties import WidgetColor
import time

# 1. Access the PVs
# pvs[0] = Vacuum (Trigger on)
# pvs[1] = sim://sine (Trigger on - acts as the clock)
# pvs[2] = loc://spike_timer_GAUCC04(0) (Storage)
try:
    sev = PVUtil.getSeverity(pvs[0])
    pulse = PVUtil.getDouble(pvs[1])
    
    # Read the last recorded spike time from our local PV
    # We use getDouble because loc:// stores numbers
    last_spike = PVUtil.getDouble(pvs[2])
    now = time.time()

    # 2. Update logic: If it's MAJOR right now, reset the 10s timer
    if sev == 2:
        last_spike = now
        pvs[2].write(now)

    # 3. Determine if we are in the "Blink Zone"
    # Either it's MAJOR now, or we are still within 10s of the last recorded MAJOR
    if sev == 2 or (now - last_spike) < 10:
        # Blink logic
        if pulse > 0:
            widget.setPropertyValue("background_color", WidgetColor(255, 0, 0)) # Bright Red
        else:
            widget.setPropertyValue("background_color", WidgetColor(100, 100, 100)) # Dark Grey
    elif sev == 1:
        widget.setPropertyValue("background_color", WidgetColor(255, 165, 0)) # Orange
    else:
        widget.setPropertyValue("background_color", WidgetColor(0, 255, 0)) # Green

except Exception as e:
    # If there's an error, turn it purple so we know it crashed
    widget.setPropertyValue("background_color", WidgetColor(255, 0, 255))