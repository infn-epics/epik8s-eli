#!/bin/bash

# put here or external
# EPICS_CA_ADDR_LIST="libera01.lnf.infn.it libera02.lnf.infn.it libera03.lnf.infn.it libera04.lnf.infn.it libera05.lnf.infn.it libera06.lnf.infn.it libera07.lnf.infn.it libera08.lnf.infn.it libera09.lnf.infn.it libera10.lnf.infn.it libera11.lnf.infn.it libera12.lnf.infn.it libera13.lnf.infn.it"
if [ ! -e "$1" ];then
    echo "* You must provide a configuration file"
    exit 1
fi
echo "* opening $1"
if [ -z "$EPICS_CA_ADDR_LIST" ];then
    docker run -it -v $(pwd):/app baltig.infn.it:4567/epics-containers/epics-py-base /venv/bin/python /app/py-ioc-collector.py -c /app/example/accumulator_orbit.json
else
    echo "setting EPICS_CA_ADDR_LIST=$EPICS_CA_ADDR_LIST"
    docker run -p 0.0.0.0:5065:5065/tcp -p 0.0.0.0:5065:5065/udp -p 0.0.0.0:5064:5064/tcp -p 0.0.0.0:5064:5064/udp -it -e EPICS_CA_ADDR_LIST="$EPICS_CA_ADDR_LIST" -v $(pwd):/app baltig.infn.it:4567/epics-containers/epics-py-base /venv/bin/python /app/py-ioc-collector.py -c /app/$1

fi
