#!/bin/bash
## current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ARCH=`uname -s`

PHOEBUS="phoebus"


if [ "$ARCH" == "Darwin" ];then
    export JAVA_HOME=/Applications/CSS_Phoebus.app/jdk/Contents/Home/
    for jar_path in \
        "/Applications/CSS_Phoebus.app/product.jar" \
        "/Applications/CSS_Phoebus.app/product-6.0.0-SNAPSHOT/product-6.0.0-SNAPSHOT.jar" \
        "/Applications/CSS_Phoebus.app/product-4.7.4-INFN/product-4.7.4-INFN.jar" \
        "/Applications/CSS_Phoebus.app/product-4.7.3/product-4.7.3.jar" \
        "/Applications/CSS_Phoebus.app/phoebus-4.7.3-SNAPSHOT/product-4.7.3-SNAPSHOT.jar" \
        "/Applications/CSS_Phoebus.app/product-4.7.4-SNAPSHOT/product-4.7.4-SNAPSHOT.jar"
    do
        if [ -f "$jar_path" ]; then
            PHOEBUS="java -jar $jar_path"
            break
        fi
    done
fi

if [ -z "$OPIHOME" ]; then
    export OPIHOME=$DIR
fi
if [ -z "$OPIDATA" ]; then
    export OPIDATA=$DIR
fi
## test if phoebus executable is found in path
if ! $PHOEBUS -h > /dev/null
then
     echo "# phoebus executable not found in PATH nor alias"
     exit

    
fi

if [ -n "$PHOEBUSINI" ];then
    echo "* USING $PHOEBUSINI"
    $PHOEBUS -settings $PHOEBUSINI -resource $OPIHOME/Launcher.bob

else
    if [ ! -f "$OPIHOME/.setting_applied" ]; then
        if [ -n "$EPICS_CA_ADDR_LIST" ]; then
            # Apply the modification
            echo "org.phoebus.pv.ca/addr_list=$EPICS_CA_ADDR_LIST" >> "$OPIHOME/settings.ini"

            # Create a marker file to indicate that the modification has been applied
            touch "$OPIHOME/.setting_applied"
        fi
        if [ -n "$EPICS_ARCHIVER" ]; then
            echo "org.csstudio.trends.databrowser3/urls=pbraw://$EPICS_ARCHIVER/retrieval" >> $OPIHOME/settings.ini
            echo "org.csstudio.trends.databrowser3/archives=pbraw://$EPICS_ARCHIVER/retrieval" >> $OPIHOME/settings.ini

            touch "$OPIHOME/.setting_applied"

        fi

        if [ -n "$CHANNEL_FINDER" ]; then
            echo "org.phoebus.channelfinder/channelfinder.service=http://$CHANNEL_FINDER/ChannelFinder" >> $OPIHOME/settings.ini
            touch "$OPIHOME/.setting_applied"
        fi

        if [ -n "$PHOEBUS_SCAN_SERVER" ]; then
            echo "org.csstudio.scan.client/host=$PHOEBUS_SCAN_SERVER" >> $OPIHOME/settings.ini
            echo "org.csstudio.scan.client/port=4810" >> $OPIHOME/settings.ini

        fi
        if [ -n "$PHOEBUS_SAVE_AND_RESTORE" ]; then
            echo "* PHOEBUS_SAVE_AND_RESTORE= $PHOEBUS_SAVE_AND_RESTORE"

            echo "org.phoebus.applications.saveandrestore.client/jmasar.service.url=http://$PHOEBUS_SAVE_AND_RESTORE/save-restore" >> $OPIHOME/settings.ini
            touch "$OPIHOME/.setting_applied"
        fi
        if [ -n "$PHOEBUS_SCAN_SERVER" ]; then
            echo "* PHOEBUS_SCAN_SERVER= $PHOEBUS_SCAN_SERVER"

            echo "org.csstudio.scan.client/host=$PHOEBUS_SCAN_SERVER" >> $OPIHOME/settings.ini
            echo "org.csstudio.scan.client/port=4810" >> $OPIHOME/settings.ini
            touch "$OPIHOME/.setting_applied"


        fi
        if [ -n "$PHOEBUS_OLOG" ]; then
            echo "* PHOEBUS_OLOG= $PHOEBUS_OLOG"    
            echo "org.phoebus.olog.es.api/olog_url=http://$PHOEBUS_OLOG/Olog" >> $OPIHOME/settings.ini
            echo "org.phoebus.olog.api/olog_url=http://$PHOEBUS_OLOG/Olog" >> $OPIHOME/settings.ini
            echo "org.phoebus.logbook/logbook_factory=olog-es" >> $OPIHOME/settings.ini
            echo "org.phoebus.olog.api/username=epics" >> $OPIHOME/settings.ini
            echo "org.phoebus.olog.api/password=epics" >> $OPIHOME/settings.ini
            touch "$OPIHOME/.setting_applied"
        fi
    
    fi

    $PHOEBUS -settings $OPIHOME/settings.ini -resource $OPIHOME/Launcher.bob 
fi
