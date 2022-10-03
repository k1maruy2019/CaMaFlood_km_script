#!/bin/sh

BASE="/usr/amoeba/pub/CaMaFlood/cmf_v401_pkg"
#EXP=$1                       # experiment name (output directory name)
YMD_STA=$1
YMD_END=$2

REGION=$3
LON1=$4
LON2=$5
LAT1=$6
LAT2=$7

YSTA=`echo ${YMD_STA} | cut -c -4 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`
MSTA=`echo ${YMD_STA} | cut -c 5-6 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`
DSTA=`echo ${YMD_STA} | cut -c 7-8 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`
#
YEND=`echo ${YMD_END} | cut -c -4 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`
MEND=`echo ${YMD_END} | cut -c 5-6 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`
DEND=`echo ${YMD_END} | cut -c 7-8 | sed 's/0*\([0-9]*[0-9]$\)/\1/g'`

ENDDATE=$(( $MEND * 100   + $DEND ))
ENDDATE=$(( $YEND * 10000 + $ENDDATE ))

SYEAR=${YSTA}
SMON=${MSTA}
SDAY=${DSTA}

SDATE=$(( $SMON  * 100   + $SDAY  ))
SDATE=$(( $SYEAR * 10000 + $SDATE ))

while [ $SDATE -lt $ENDDATE ];
do
    SCHH="00"
    CDATE_1="${SDATE}${SCHH}"
    echo "./jma_warnflood_vis_nc_region.py $EXP $CDATE_1 $REGION $LON1 $LON2 $LAT1 $LAT2"
    ./jma_warnflood_vis_nc_region.py $CDATE_1 $REGION $LON1 $LON2 $LAT1 $LAT2
##
    SYEAR=${SYEAR}
    SMON=${SMON}
    SDAY=${SDAY}
    SDAY=$(( $SDAY + 1 ))

    NSDAY=`$BASE/util/igetday $SYEAR $SMON`
    if [ $SDAY -gt $NSDAY ]; then
	SDAY=1
	SMON=$(( $SMON + 1 ))
    fi
    if [ $SMON -gt 12 ]; then
	SMON=1
	SYEAR=$(( $SYEAR +1 ))
    fi

    SDATE=$(( $SMON  * 100   + $SDAY  ))
    SDATE=$(( $SYEAR * 10000 + $SDATE ))
done

exit 0

