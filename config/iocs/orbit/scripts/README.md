# py-ioc-collector
This python IOC collects PVs in an array. The new PVs to create and the connection are specified in a JSON file (see example).

The following example create an ioc with prefix *accumulator:orbit:* and create *x* *y* array from other PVs.
It's possible to modify the *src* values by providing a global or vector *coeff* that multiply values and *off* to add an offset to values.
It's possible also create *constant* PVs array.
For each new PV it's possible to specify a refresh rate in ms *update*, the *src* values will be sampled every *update* ms.

```
{
    "prefix":"accumulator:orbit:",
    "collect":[
    {
        "pvname":"x",
        "src":["LIBERA08:SA:SA_X_MONITOR","LIBERA07:SA:SA_X_MONITOR","libera13:bpm1:sa.X","libera13:bpm2:sa.X","LIBERA01:SA:SA_X_MONITOR","LIBERA02:SA:SA_X_MONITOR","LIBERA09:SA:SA_X_MONITOR","libera12:bpm2:sa.X","libera12:bpm4:sa.X","libera12:bpm1:sa.X","libera12:bpm3:sa.X","LIBERA03:SA:SA_X_MONITOR"],
        "coeff":0.001,
        "type":"float",
        "update":1000
    },
    {
        "pvname":"y",
        "src":["LIBERA08:SA:SA_Y_MONITOR","LIBERA07:SA:SA_Y_MONITOR","libera13:bpm1:sa.Y","libera13:bpm2:sa.Y","LIBERA01:SA:SA_Y_MONITOR","LIBERA02:SA:SA_Y_MONITOR","LIBERA09:SA:SA_Y_MONITOR","libera12:bpm2:sa.Y","libera12:bpm4:sa.Y","libera12:bpm1:sa.Y","libera12:bpm3:sa.Y","LIBERA03:SA:SA_Y_MONITOR"],
        "coeff":0.001,
        "type":"float",
        "update":500
    },
    {
        "pvname":"coord",
        "const":[2.801375,5.206375,6.577375,9.704125,11.075125,13.480125,17.721875, 19.082875, 22.858875,25.985625,29.761625,31.122625],
        "update":0
    },
    {
        "pvname":"bpm",
        "type": "string",
        "const":["BPBA1001","BPSA1001","BPBA1002","BPBA2001","BPSA2001","BPBA2002","BPBA3001", "BPSA3001", "BPBA3002","BPBA4001","BPSA4001","BPBA4002"],
        "update":0
    }


]
}
```


## Getting started

### Requirements
A epics installation available in path.

### Run on host
```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python py-ioc-collector.py -c example/accumulator_orbit.json

```

### Run in docker
Set optional environment variable *EPICS_CA_ADDR_LIST* per accedere alle PVs.

example:
```
export EPICS_CA_ADDR_LIST="libera01.lnf.infn.it libera02.lnf.infn.it libera03.lnf.infn.it libera04.lnf.infn.it libera05.lnf.infn.it libera06.lnf.infn.it libera07.lnf.infn.it libera08.lnf.infn.it libera09.lnf.infn.it libera10.lnf.infn.it libera11.lnf.infn.it libera12.lnf.infn.it libera13.lnf.infn.it"

./run_in_docker.sh example/accumulator_orbit.json
```

### Development
Use the *.devcontainer.json* by opening this folder in container

