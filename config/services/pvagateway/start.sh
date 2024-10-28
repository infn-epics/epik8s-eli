#!/bin/sh
name=`hostname`
echo "Starting PVA Gateway ($name)"
# -debug 1
CLIENT_NAME="$name"
#export EPICS_PVA_ADDR_LIST $EPICS_CA_ADDR_LIST
export EPICS_PVA_NAME_SERVERS=$EPICS_PVA_ADDR_LIST
# Generate JSON content
JSON_CONTENT=$(cat <<EOF
{
    "version": 2,
    "clients":[
        {
            "name":"internal",
            "addrlist": "$EPICS_PVA_NAME_SERVERS",
            "autoaddrlist":false
        }
        

    ],
    "servers": [

        {
            "name":"localhost",
            "clients":["internal"],
            "autoaddrlist":false,
            "statusprefix":"GW:STS:"
        }
    ]
}
EOF
)



# Output the JSON content to a file
echo "$JSON_CONTENT" > gateway_config.json

echo "Generated gateway_config.json:"
cat gateway_config.json
## -- debug
python3 -m p4p.gw gateway_config.json
