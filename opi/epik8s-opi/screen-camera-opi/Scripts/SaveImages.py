from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from java.lang import Thread

logger = ScriptUtil.getLogger()
mydev = widget.getEffectiveMacros().getValue("DEVICE")
mycam = widget.getEffectiveMacros().getValue("CAM")
start_save = PVUtil.getDouble(pvs[0])

if start_save==1 and mydev and mycam:
    # Scalars go over PVA; the char-waveform strings (FileName, FileTemplate)
    # stay on CA, since PVA delivers them as byte arrays.
    prefx="pva://"+mydev+':'+mycam+":TIFF1:"
    prefx_ca="ca://"+mydev+':'+mycam+":TIFF1:"
    TMO=3000  # ms; 100 ms was too short for a first connection
    #start acquire
    pv00=PVUtil.createPV("pva://"+mydev+':'+mycam+":Acquire",TMO)
    pv00.setValue(1)
    pv0=PVUtil.createPV(prefx_ca+"FileName",TMO)
    pv0.setValue("img")
    pv1=PVUtil.createPV(prefx+"FileNumber",TMO)
    pv1.setValue(0)
    pv2=PVUtil.createPV(prefx+"AutoIncrement",TMO)
    pv2.setValue(1)
    pv3=PVUtil.createPV(prefx_ca+"FileTemplate",TMO)
    pv3.setValue("%s%s%3.3d.tiff")
    pv4=PVUtil.createPV(prefx+"FileWriteMode",TMO)
    pv4.setValue(1)  # FileWriteMode: 0=Single 1=Capture 2=Stream
    pv5=PVUtil.createPV(prefx+"AutoSave",TMO)
    pv5.setValue(0)
    pv6=PVUtil.createPV(prefx+"Capture",TMO)
    pv7=PVUtil.createPV(prefx+"Capture_RBV",TMO)
    pv8=PVUtil.createPV(prefx+"NumCapture_RBV",TMO)
    pv9=PVUtil.createPV(prefx+"NumCaptured_RBV",TMO)
    pv10=PVUtil.createPV(prefx+"WriteFile",TMO)
    nimg=PVUtil.getInt(pv8);
    max_attempts=20*nimg
    Thread.sleep(500)
    pv6.setValue(1)

    attempts=0
    while attempts<max_attempts:
        pv_value=PVUtil.getInt(pv9)
        #print(pv_value)
        if pv_value == nimg:
            print("While loop break condition reached")
            Thread.sleep(500)
            pv10.setValue(1)
            print("Images saved!")
            break
        else:
            pass;
        
        attempts += 1
        Thread.sleep(100)  # argument is in milliseconds
    else:
        print("Device not ready after all the attempts")
        pv6.setValue(0) #stop Capture

    #at the end put back to 0
    pvs[0].write(0);
elif start_save==1:
    #DEVICE/CAM not resolved yet (e.g. camera panel still reloading): bail out
    #without saving, but clear the button so it isn't left stuck at 1
    pvs[0].write(0);
else:
	pass
