#!/bin/bash
# TOTAL RUNOFF 

homedata="/usr/amoeba/pub/CaMaFlood/TE/data"
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

for j in ro tp; do
    sdir=`echo ${dirs[$j]} | tr '[:upper:]' '[:lower:]'`
    subdir="${homedata}/${date}/${dirs[$j]}"
    echo $subdir
    mkdir -p $subdir
    INPUT="$subdir/${sdir}_${date}.bin"
    echo $INPUT
    mv $subdir/${sdir}_$date.bin /usr/amoeba/pub/CaMaFlood/inp/TE
done
