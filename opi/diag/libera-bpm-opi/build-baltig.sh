#!/bin/bash
docker build -f Dockerfile -t baltig.infn.it:4567/lnf-da-control/dcs-control-console/bpmedm:latest .
docker push baltig.infn.it:4567/lnf-da-control/dcs-control-console/bpmedm:latest

# docker build -t baltig.infn.it:4567/lnf-da-control/dcs-control-console/ubuntu:latest .
# docker push baltig.infn.it:4567/lnf-da-control/dcs-control-console/ubuntu:latest
