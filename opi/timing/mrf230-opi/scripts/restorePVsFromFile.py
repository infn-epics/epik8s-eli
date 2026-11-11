from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
#from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, DataUtil

# logger = ScriptUtil.getLogger()
device_prefix = widget.getEffectiveMacros().getValue("P")

# logger.info("device " +device_prefix )

name = PVUtil.getString(pvs[0])

# pv = ScriptUtil.getPrimaryPV(filename)
# name = PVUtil.getString(pv)
print "Loading: "+name
delays =  ScriptUtil.findWidgetByName(widget, "Delay")

if name:
    #os.makedirs(os.path.dirname(name), exist_ok=True)
    print "selected path:"+name
                 
    # Open the file for writing
    with open(name, 'r') as file:
        # Loop over the 16 PVs and write their values to the file
        for line in file:
        # Strip any leading/trailing whitespace characters
            line = line.strip()
            if line:  # Check if line is not empty
                # Split the line by the comma
                key, value = line.split(',', 1)
                # Store the key-value pair in the dictionary
                pvn="loc://apply_"+key
                print "setting : "+ pvn +" = "+ value
                loc_pv = PVUtil.createPV(pvn,1)
                # value = PVUtil.getString(pv)
            
                loc_pv.write(value)

    #     # Write the filename to the PV
                                 
        ScriptUtil.showMessageDialog(widget,"Loaded "+name)
        
   
