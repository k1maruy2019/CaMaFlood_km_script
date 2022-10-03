#!/bin/bash
# TOTAL RUNOFF 

home='/usr/amoeba/pub/CaMaFlood/TE'
homedata="${home}/data"

declare -A dirs=(
    ["ro"]="RUNOFF"
    ["tp"]="GPRCT"
)

if [ $# -eq 0 ]; then
    exit
else
    date=$1
    YEAR=${date:0:4}
    MON=${date:4:2}
    DAY=${date:6:2}
    echo "$YEAR/$MON/$DAY"
fi

aws s3 sync s3://dev-wfc-flood-products/CaMaFlood/TE/data/${date}/ ${homedata}/${date}/









