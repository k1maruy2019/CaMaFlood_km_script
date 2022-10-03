#!/bin/bash

date0=$1
for i in $(seq 0 ${2})
do
    datei=`date "+%Y%m%d" --date "$i days ${date0}"`
    /usr/amoeba/pub/CaMaFlood/ECMWF/rotp_convert_nocurl_aws.sh $datei
    echo "ecmwf.free.pp_runoff.sh $datei"
    ./ecmwf.free.pp_runoff.sh $datei
done



