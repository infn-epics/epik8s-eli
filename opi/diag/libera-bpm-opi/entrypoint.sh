#!/bin/bash

set -e
echo "* Starting $IGPTOP/bin/edm $BPMTYPE on DEVICE = $DEVICE "
if [ -f $IGPTOP/config/epics_addr_list ]; then
    export EPICS_CA_ADDR_LIST=`cat epics_addr_list`
    export EPICS_CA_AUTO_ADDR_LIST="NO"
    echo "* Setting EPICS_CA_ADDR_LIST=$EPICS_CA_ADDR_LIST"
fi
#export LD_LIBRARY_PATH="$LD_LIBRARY_PATH $IGPTOP/extensions/lib/linux-x86"
export EDM_TOPDIR=$(pwd)/$BPMTYPE
export EDMDATAFILES=$EDM_TOPDIR/panels
export EDMOBJECTS=$EDM_TOPDIR/prefs
export EDMFILES=$EDM_TOPDIR/prefs
export EDMPVOBJECTS=$EDM_TOPDIR/prefs
export EPICS_CA_MAX_ARRAY_BYTES=5000000
export EPICS_HOST_ARCH=linux-x86
$IGPTOP/bin/edm -cmap -x -noedit -m "DEVICE=$DEVICE" $BPMTYPE/panels/main.edl


