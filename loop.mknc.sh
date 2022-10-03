#!/bin/sh

BASE="/usr/amoeba/pub/CaMaFlood/cmf_v401_pkg"
EXP=$1                       # experiment name (output directory name)
YMD_STA=$2
YMD_END=$3

#REGION=$4
#LON1=$5
#LON2=$6
#LAT1=$7
#LAT2=$8

YSTA=2022                                   # start year ( from YSTA / Jan  1st _ 00:00) (maruya Edit)
MSTA=8                                                                                   
DSTA=25
YEND=2022                                   # end   year (until YEND / Dec 31st _ 24:00) (maruya Edit) 
MEND=9
DEND=1
#SPINUP=0                                    # [0]: zero-storage start, [1]: from restart file
#NSP=0                                       # spinup repeat time
#
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
SHOUR=6

EYEAR=${SYEAR}
EMON=${SMON}
EDAY=$(( $SDAY + 1 ))     ## 39hr simulation
EHOUR=$(( $SHOUR + 15 ))
if [ $EHOUR -ge 24 ]; then
  EDAY=$(( $EDAY + 1 ))
  EHOUR=$(( $EHOUR - 24 ))
fi

SDATE=$(( $SMON  * 100   + $SDAY  ))
SDATE=$(( $SYEAR * 10000 + $SDATE ))
SCHH=`printf %02d ${SHOUR}`

EDATE=$(( $EMON  * 100   + $EDAY  ))
EDATE=$(( $EYEAR * 10000 + $EDATE ))
ECHH=`printf %02d ${EHOUR}`

while [ $EDATE -lt $ENDDATE ];
do
    CDATE_0="${SDATE}"	 
    CDATE="${SDATE}${SCHH}00"
    echo "./camaflood_post_mknetcdf.py $EXP $CDATE"
    ./camaflood_post_mknetcdf.py $EXP $CDATE    
#    echo "./camaflood_post_vis_nc.py $EXP $CDATE"
#    ./camaflood_post_vis_nc.py $EXP $CDATE
#    echo "./camaflood_post_vis_nc_region.py $EXP $CDATE $REGION $LON1 $LON2 $LAT1 $LAT2"
#    ./camaflood_post_vis_nc_region.py $EXP $CDATE $REGION $LON1 $LON2 $LAT1 $LAT2
    if [ $SCHH == "06" ]; then       
	echo "ec_rotp_aws.sh $CDATE"
#       ./ec_rotp_aws.sh $CDATE
	echo "te_rotp_aws.sh $CDATE"
#       ./te_rotp_aws.sh $CDATE
#       echo "./camaflood_te_vis_nc_region.py $EXP $CDATE $REGION $LON1 $LON2 $LAT1 $LAT2"
#       ./camaflood_te_vis_nc_region.py $EXP $CDATE_0 $REGION $LON1 $LON2 $LAT1 $LAT2
#       echo "./camaflood_ec_vis_nc_region.py $EXP $CDATE $REGION $LON1 $LON2 $LAT1 $LAT2"
#       ./camaflood_ec_vis_nc_region.py $EXP $CDATE_0 $REGION $LON1 $LON2 $LAT1 $LAT2
    fi
##
    SYEAR=${SYEAR}
    SMON=${SMON}
    SDAY=${SDAY}
    SHOUR=$(( $SHOUR + 12 ))   ## advance 12hr
    if [ $SHOUR -ge 24 ]; then
	SDAY=$(( $SDAY + 1 ))
	SHOUR=$(( $SHOUR - 24 ))
    fi
    NSDAY=`$BASE/util/igetday $SYEAR $SMON`
    if [ $SDAY -gt $NSDAY ]; then
	SDAY=1
	SMON=$(( $SMON + 1 ))
    fi
    if [ $SMON -gt 12 ]; then
	SMON=1
	SYEAR=$(( $SYEAR +1 ))
    fi

    EYEAR=${SYEAR}
    EMON=${SMON}
    EDAY=$(( $SDAY + 1 ))     ## 39hr simulation
    EHOUR=$(( $SHOUR + 15 ))
    if [ $EHOUR -ge 24 ]; then
	EDAY=$(( $EDAY + 1 ))
	EHOUR=$(( $EHOUR - 24 ))
    fi
    NEDAY=`$BASE/util/igetday $EYEAR $EMON`
    if [ $EDAY -gt $NEDAY ]; then
	EDAY=1
	EMON=$(( $EMON + 1 ))
    fi
    if [ $EMON -gt 12 ]; then
	EMON=1
	EYEAR=$(( $EYEAR +1 ))
    fi
    
    SDATE=$(( $SMON  * 100   + $SDAY  ))
    SDATE=$(( $SYEAR * 10000 + $SDATE ))
    SCHH=`printf %02d ${SHOUR}`
    
    EDATE=$(( $EMON  * 100   + $EDAY  ))
    EDATE=$(( $EYEAR * 10000 + $EDATE ))
    ECHH=`printf %02d ${EHOUR}`
done

exit 0

