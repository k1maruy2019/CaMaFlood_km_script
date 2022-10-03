#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pprint
pprint.pprint(sys.path)
import xarray as xr
import datetime

import cartopy.crs as ccrs
import cartopy.util as cutil
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import subprocess

XSIZE=1500
YSIZE=1320
datasize4=XSIZE*YSIZE*4
datasize=XSIZE*YSIZE

lon0=123
lon1=148
#div_lon=0.4
div_lon=1/60
lat0=24
lat1=46
div_lat=0.4
div_lat=1/60
N_lon=int((lon1-lon0)/div_lon)
N_lat=int((lat1-lat0)/div_lat)

lat1d=[ lat0+i*div_lat for i in range(0,N_lat)]
lon1d=[ lon0+i*div_lon for i in range(0,N_lon)]
#lat1d=[ lat0+i*div_lat for i in range(N_lat+1)]
#lon1d=[ lon0+i*div_lon for i in range(N_lon+1)]

args=sys.argv
home='/usr/amoeba/pub/CaMaFlood/out/'
homenc='/usr/amoeba/pub/CaMaFlood/outnc/'

projname="test3-jpn_fcast_EC/"
projname=args[1]
date0=args[2]
#time0=args[3]
dt0=datetime.datetime.strptime(date0,"%Y%m%d%H%M%S")
date0=dt0.strftime("%Y%m%d%H")
date1=dt0.strftime("%Y%m%d%H")
print("date0=",date0)

dir_outnc=f'{homenc}{projname}/{date0}'
#dir_outnc=f'{homenc}{projname}{date0}{time0}'


os.makedirs(dir_outnc,exist_ok=True)

#date1=args[2]
ihour=0
varlist=("flddph","maxdph","outflw", "storge","fldfrc")
#leveldict={}
#leveldict["flddph"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
#leveldict["maxdph"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
#leveldict["outflw"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
#leveldict["storge"]=np.arange(0,1000,100)
#leveldict["fldfrc"]=np.arange(0,1,0.1)
unitdict={}
unitdict["flddph"]="m"
unitdict["maxdph"]="m"
unitdict["outflw"]="m3/s"
unitdict["storge"]="m3"
unitdict["fldfrc"]="m2/m2"

import datetime
import pandas as pd

#print(args)

#date_=f'{data0}{time0}'


dt1=dt0

for var in varlist:
    vardata2d=[]
    time0=[]
    for ihour in range(0,17):
        print("ihour=",ihour+1)
        varbin=f'{var}{date0}.bin'
        head=f'{home}{projname}/{date0}/'
        binfile=f'{head}{varbin}'
        print(binfile)
        tmpihourbin=f'tmp{ihour}.bin'
        subprocess.call(f'/usr/amoeba/pub/CaMaFlood/script/yrev_it {binfile} ./{tmpihourbin} {XSIZE} {YSIZE} {ihour}',shell=True)
#        subprocess.call(f'mv /usr/amoeba/pub/CaMaFlood/script/tmp.bin ./{tmpihourbin}',shell=True)
        varfp=open(f'./{tmpihourbin}',"rb")

        vardata=np.fromfile(varfp,dtype='<f',sep='',count=datasize).reshape(YSIZE,XSIZE)
        xmask=vardata>999
        vardata[xmask]=np.nan
        vardata2d.append(vardata.reshape(YSIZE,XSIZE))
        #
        dt1=dt1+datetime.timedelta(hours=1)
        date1=dt1.strftime("%Y%m%d%H")
        time0.append(dt1)
        subprocess.call(f'rm ./{tmpihourbin}',shell=True)
    datetime_array=pd.to_datetime(time0)
    xrdata=xr.DataArray(vardata2d,name=var,
                        coords={'time':datetime_array,
                                        'lat':lat1d,'lon':lon1d},
                        dims=['time','lat','lon'])
    ncfile=f'{dir_outnc}/{var}_{date0}.nc'
    xrdata.to_netcdf(ncfile)

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        projname=args[1]
        date0=args[2]        
        print(date0)
    else:
        print('Arguments are too short')


    

