#!/opt/libera-ioc/bin/liberaIOC

# -------------------------------- HEADER -------------------------------------

## You may have to change liberaIOC to something else
## everywhere it appears in this file

epicsEnvSet("ARCH","linux-x86")
epicsEnvSet("TOP","__IOC_TOP__")
epicsEnvSet("ASYN","/opt/epics/asyn")
epicsEnvSet("EPICS_BASE","/opt/epics/base")

cd ${TOP}

## Import IOC name that sets IOCNAME env variable
# Set default IOC name (if tmp/IOCname.env not present)
epicsEnvSet("IOCNAME","__IOC_PREFIX__")
# Get IOC name from tmp/IOCname.env (generated from IOCname)

## Register all support components
dbLoadDatabase("dbd/liberaIOC.dbd")
liberaIOC_registerRecordDeviceDriver(pdbbase)

## Asyn traces
# Turn on global trace
#asynSetTraceMask("", 0, 255)
# Turn off global trace
asynSetTraceMask("", 0, 0)
# ------------------------ SPE SPECIFIC ---------------------------------------

epicsEnvSet("MCIAPP","libera-spe")

## Load record instances
# Libera MCI tree support

dbLoadRecords("db/spe.db",                  "P=${IOCNAME},D=${MCIAPP}")

dbLoadRecords("db/gdx.db",                  "P=${IOCNAME},D=${MCIAPP},MB=gdx1,B=gdx")
dbLoadRecords("db/evrx.db",                 "P=${IOCNAME},D=${MCIAPP},MB=evrx2,B=evrx")

dbLoadRecords("db/rfspe.db",                "P=${IOCNAME},D=${MCIAPP},MB=rfspe3,B=__BPM1__")
dbLoadRecords("db/rfspe.db",                "P=${IOCNAME},D=${MCIAPP},MB=rfspe4,B=__BPM2__")
dbLoadRecords("db/rfspe.db",                "P=${IOCNAME},D=${MCIAPP},MB=rfspe5,B=__BPM3__")
dbLoadRecords("db/rfspe.db",                "P=${IOCNAME},D=${MCIAPP},MB=rfspe6,B=__BPM4__")

## Asyn record for Libera asyn driver
dbLoadRecords("/opt/epics/asyn/db/asynRecord.db","P=${IOCNAME}:,R=${MCIAPP}:asyn,PORT=${MCIAPP},ADDR=0,IMAX=100,OMAX=100")

## Configure Libera port driver
# Several Libera base based application can be accessed by specifying Asyn
# port as the application name - see MCI app-name node that each Libera base
# application provides.

# initLibera() arguments:
#   a_portName  - the name to give to this asyn port driver

initLibera("${MCIAPP}")

# Turn on port traces
#asynSetTraceMask("${MCIAPP}", 0, 0xff)
#asynSetTraceIOMask("${MCIAPP}", 0, 0xff)

# Turn off port traces
asynSetTraceMask("${MCIAPP}", 0, 0)
asynSetTraceIOMask("${MCIAPP}", 0, 0)

# ------------------------ PLATFORM SPECIFIC ----------------------------------

## Load record instances
# Libera MCI tree support
dbLoadRecords("db/static.db",         "P=${IOCNAME},D=libera-platform")
dbLoadRecords("db/platform.db",       "P=${IOCNAME},D=libera-platform")

dbLoadRecords("db/os_sensors.db",     "P=${IOCNAME},D=libera-platform,MB=os,B=os")
dbLoadRecords("db/icb_sensors.db",    "P=${IOCNAME},D=libera-platform,MB=icb0,B=icb")
dbLoadRecords("db/gdx_sensors.db",    "P=${IOCNAME},D=libera-platform,MB=gdx1,B=gdx")
dbLoadRecords("db/evrx_sensors.db",   "P=${IOCNAME},D=libera-platform,MB=evrx2,B=evrx")
#dbLoadRecords("db/tim_sensors.db",    "P=${IOCNAME},D=libera-platform,MB=tim2,B=tim")
dbLoadRecords("db/rfspe_sensors.db",  "P=${IOCNAME},D=libera-platform,MB=rfspe3,B=__BPM1__")
dbLoadRecords("db/rfspe_sensors.db",  "P=${IOCNAME},D=libera-platform,MB=rfspe4,B=__BPM2__")
dbLoadRecords("db/rfspe_sensors.db",  "P=${IOCNAME},D=libera-platform,MB=rfspe5,B=__BPM3__")
dbLoadRecords("db/rfspe_sensors.db",  "P=${IOCNAME},D=libera-platform,MB=rfspe6,B=__BPM4__")

## Asyn record for Libera asyn driver
dbLoadRecords("/opt/epics/asyn/db/asynRecord.db","P=${IOCNAME}:,R=libera-platform:asyn,PORT=libera-platform,ADDR=0,IMAX=100,OMAX=100")

## Configure Libera port driver
# Several Libera base based application can be accessed by specifying Asyn
# port as the application name - see MCI app-name node that each Libera base
# application provides.

# initLibera() arguments:
#   a_portName  - the name to give to this asyn port driver

initLibera("libera-platform")

# Turn on port traces
#asynSetTraceMask("libera-platform", 0, 0xff)
#asynSetTraceIOMask("libera-platform", 0, 0xff)

# Turn off port traces
asynSetTraceMask("libera-platform", 0, 0)
asynSetTraceIOMask("libera-platform", 0, 0)

# -------------------------------- FOOTER -------------------------------------

# Save list of PVs to a file
dbl > pvlist.txt

iocInit()
