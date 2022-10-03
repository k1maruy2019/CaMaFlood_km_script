#!/bin/bash

date=$1
./p0_runoff.py $date "03"
mv masked_rev.bin runoff_$date.bin
for i in `seq 3 3 24`; do
    ii=`printf "%02d" $(($i))`
    jj=`printf "%02d" $(($i+3))`
    ./pp_runoff.py $date $ii $jj
    cat masked_rev.bin >> runoff_$date.bin
done
mv runoff_$date.bin /usr/amoeba/pub/CaMaFlood/inp/ECMWF.free
/usr/bin/rm -rf /usr/amoeba/pub/CaMaFlood/ECMWF.free/$date


