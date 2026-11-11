from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.model.properties import WidgetColor

try:
    # 1. Inputs
    labels = PVUtil.getStringArray(pvs[0])
    tsh_values = PVUtil.getDoubleArray(pvs[1])
    pump_pvs = pvs[2:]
    
    # 2. Retrieve previous values for trend calculation
    # Store as a dict: { 'label': last_value }
    history = widget.getVar("history")
    if history is None:
        history = {}

    raw_data = []

    # 3. Process each pump
    for i in range(len(labels)):
        if i < len(pump_pvs):
            current_val = PVUtil.getDouble(pump_pvs[i])
            label = labels[i]
            
            # Determine Trend
            prev_val = history.get(label, current_val)
            if current_val > prev_val * 1.01: # 1% increase threshold to avoid noise
                trend = "↑ RISING"
            elif current_val < prev_val * 0.99:
                trend = "↓ FALLING"
            else:
                trend = "↔ STABLE"
            
            # Update history for next execution
            history[label] = current_val

            raw_data.append({
                'label': label,
                'value': current_val,
                'threshold': tsh_values[i] if i < len(tsh_values) else 1e-7,
                'trend': trend
            })

    widget.setVar("history", history)

    # 4. Sort: Worst pressure first
    raw_data.sort(key=lambda x: x['value'], reverse=True)

    # 5. Build Table Rows and Color Cells
    final_table_values = []
    for i, item in enumerate(raw_data):
        val_str = "{:.2e}".format(item['value'])
        tsh_str = "{:.2e}".format(item['threshold'])
        
        # Add to table: [Name, Pressure, Threshold, Trend]
        final_table_values.append([item['label'], val_str, tsh_str, item['trend']])

        # Color Logic
        if item['value'] >= item['threshold']:
            row_color = WidgetColor(255, 0, 0)      # Red
        elif item['value'] >= (item['threshold'] * 0.1):
            row_color = WidgetColor(255, 165, 0)    # Orange
        else:
            row_color = WidgetColor(0, 220, 0)      # Green

        # Apply color to all 4 columns
        for col in range(4):
            widget.setCellColor(i, col, row_color)

    widget.setValue(final_table_values)

except Exception as err:
    print("Trend Table Error: " + str(err))