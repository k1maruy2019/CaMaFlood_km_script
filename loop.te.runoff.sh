#!/bin/bash

date0=$1
for i in $(seq 0 ${2})
do
    datei=`date "+%Y%m%d" --date "$i days ${date0}"`
    /usr/amoeba/pub/CaMaFlood/TE/script/te_rotp_download_aws.sh $datei
done
