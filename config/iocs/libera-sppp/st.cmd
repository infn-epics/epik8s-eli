#!/opt/epics-libera/bin/linux-arm/libera

epicsEnvSet(ARCH,"linux-arm")
epicsEnvSet(IOC,"__IOC_NAME__")
epicsEnvSet(TOP,"__IOC_TOP__")
epicsEnvSet(EPICS_BASE,"/opt/epics-libera")
cd ${TOP}

## Register all support components
dbLoadDatabase("dbd/liberaSupport.dbd",0,0)
liberaSupport_registerRecordDeviceDriver(pdbbase)

### PORT INITIALIZATION

# Environment port
liberaInit("ENV","ENV", "0", "0", "0", "0", "1")

# Fast Application port reading/writing 8192 samples
liberaInit("FA","FA", "0", "8192", "0", "0", "1")

# ADC port reading 1024 samples
liberaInit("ADC","ADC", "0", "1024", "0", "0", "1")

# Slow Acquisition port
liberaInit("SA","SA", "0", "0", "0", "0", "1")

#asynSetTraceMask("SA",0,0x1f)
#asynSetTraceIOMask("SA",0,0x7)

## Load record instances
cd db
dbLoadTemplate("libera.substitutions")

cd ${TOP}
iocInit()
dbl > pvlist.txt
