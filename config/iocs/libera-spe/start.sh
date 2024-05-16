#!/bin/bash
mount -o remount ,rw /
kill -9 "$(pidof procServ)" 2>/dev/null >/dev/null
echo "server 193.206.84.121" > /openntpd/ntpd.conf
echo "server 193.206.84.122" >> /openntpd/ntpd.conf
echo "server 193.206.84.123" >> /openntpd/ntpd.conf
ntpd -s
/etc/init.d/libera-ioc stop

variables=( "__IOC_PREFIX__" "__IOC_TOP__" "__IOC_NAME__" "__BPM1__" "__BPM2__" "__BPM3__" "__BPM4__")

# Loop through each variable
for var in "${variables[@]}"; do
    # Check if the variable is defined and non-empty
    if [ -n "${!var}" ]; then
        echo "patching $var ${!var}"
        # Use sed to replace the variable in the specified files
        sed -i "s|$var|${!var}|g" db/* *.cmd
    else
        echo "%%Warning no $var defined"
    fi
done

# If you have more than one ethernet interface you must specify
# the following environment variable. We do not want the CA server
# responding multiple times!!
# export EPICS_CAS_INTF_ADDR_LIST=<IP number of your primary network card>
# Please consult the EPICS software manager for the proper command # here:
# --- OPTIONAL ---
# export EPICS_CAS_INTF_ADDR_LIST=172.31.75.3

# Libera EPICS IOC top install folder
TOP=$__IOC_TOP__
PROCSERV=/usr/bin/procServ
PORT=4050
NAME=$__IOC_NAME__
PID=/var/run/libera-ioc.pid
PROCARGS="-q -c $TOP -i ^D^C^] -p $PID -n $NAME --restrict -f"
LI="/opt/libera/bin/libera-ireg"

[ ! -d "$TOP" ] && exit 1
[ ! -f "$PROCSERV" ] && exit 1

cd $TOP

# Fixup system date if needed, EPICS is very picky about it and we need to
# be at least in the year 2000, so make it 2010.. ;)
_stamp2000=$(date -d "00:00:00 2000-01-01 UTC" +%s)
_stampNow=$(date +%s)
if [ $_stampNow -lt $_stamp2000 ]; then
	date 010100002010.00 2>/dev/null >/dev/null
	echo "WARNING - Libera system date : $(date)"
fi

# Make IOC name environment variable for IOC. Value is read from file IOCname,
# if exists, else it is set to default value: LIBERA01.
# Only first line of IOCname file is read, and no restrictions are applied to
# the IOC name at this point, consult EPICS documentation for more information.
IOCNAME=$__IOC_PREFIX__

echo " -> IOC name $IOCNAME"

# Start the caRepeater in the background
if [ -f /opt/epics/base/bin/caRepeater ]; then 
	/opt/epics/base/bin/caRepeater >/dev/null 2>&1 </dev/null&
fi

# production:
export EPICS_CA_MAX_ARRAY_BYTES=5000000
$PROCSERV $PROCARGS $PORT $TOP/st.cmd

# debug:
# export EPICS_CA_MAX_ARRAY_BYTES=35000000
# export PROCSERV_DEBUG=yes
# exec procServ <port> exec $PROCARGS $PORT st.cmd > procServ.log </dev/null 2>&1 &
# Access this IOC using 'telnet localhost <port>'

