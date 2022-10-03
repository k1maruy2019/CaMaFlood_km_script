#!/bin/bash

declare -A dirs=(
    ["index"]="INDEX"
    ["ro"]="RUNOFF"
    ["tp"]="TPRCT"
)

home='/usr/amoeba/pub/CaMaFlood/ECMWF.free'
start=49738258
length=609070 
end=$(($start+$length))
ROOT="https://data.ecmwf.int/forecasts"
date=20220712
date=$1
hh=00z
lon1=122
lon2=148
lat1=24
lat2=46

#for j in index ro tp; do
#aws s3 sync s3://dev-wfc-flood-products/CaMaFlood/ECMWF.free/${date}/${dirs[$j]} ${home}/${date}/${dirs[$j]}
#done

aws s3 sync s3://dev-wfc-flood-products/CaMaFlood/ECMWF.free/${date}/ ${home}/${date}/





