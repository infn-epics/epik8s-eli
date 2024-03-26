#!/root/redpitaya-ioc/bin/linux-arm/RedPitayaTest

< envPaths
epicsEnvSet currdir ${PWD}
cd ${TOP}

## Register all support components
dbLoadDatabase("dbd/RedPitayaTest.dbd",0,0)
RedPitayaTest_registerRecordDeviceDriver(pdbbase) 

RedPitaya_Initialise (4)

# RedPitaya_Configure (portName, triggerPollingInterval in seconds)
RedPitaya_Configure ("RP", 0.1)
## Load record instances
dbLoadTemplate("${currdir}/redpitaya.substitutions")

iocInit()
dbl
# end
