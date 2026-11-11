ARCH=`uname -s`
xhost +
if [ "$ARCH" == "Darwin" ];then
    kill -9 `lsof  -i tcp:6000 | tail -1 | cut -d ' ' -f 4`
    cnt=0
    IP=""
    while [ -z "$IP" ] && [ $cnt -lt 10 ] ;do
        echo "* looking interface en$cnt"
        IP=`ipconfig getifaddr en$cnt`
        ((cnt++))

    done
    if [ -n $IP ];then

        socat TCP-LISTEN:6000,bind=$IP,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &
        export DISPLAY=$IP:0.0
        echo "* forwarding on $DISPLAY"
    else
        echo "## cannot find valid IP to forward DISPLAY"
        exit 1
    fi
fi
docker run --name bpm -u `id -u`:`id -g` -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix baltig.infn.it:4567/lnf-da-control/dcs-control-console/bpmedm:latest
