#!/usr/bin/env python
# coding: utf-8
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cartopy.util as cutil
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import datetime

import subprocess

args=sys.argv

home='/usr/amoeba/pub/CaMaFlood/out/'
homenc='/usr/amoeba/pub/CaMaFlood/outnc/'
homefig='/usr/amoeba/pub/CaMaFlood/outfig/'
#projname="test3-jpn_fcast_EC/"
projname=args[1]

#date=2022071906
date=args[2]

#dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M%S")
dt0=datetime.datetime.strptime(date,"%Y%m%d%H")
date=dt0.strftime("%Y%m%d%H")
print(date)

dir_outnc=f'{homenc}{projname}/{date}'
dir_outfig=f'{homefig}{projname}/{date}'

os.makedirs(dir_outfig,exist_ok=True)


ihour=0
varlist=("flddph","maxdph","outflw", "storge","fldfrc")
leveldict={}
leveldict["flddph"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
leveldict["maxdph"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
leveldict["outflw"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
leveldict["storge"]=np.arange(0,1000,100)
leveldict["fldfrc"]=np.arange(0,1,0.1)
unitdict={}
unitdict["flddph"]="m"
unitdict["maxdph"]="m"
unitdict["outflw"]="m3/s"
unitdict["storge"]="m3"
unitdict["fldfrc"]="m2/m2"


for var in varlist:
#    varbin=f'{date}/{var}{date}.bin'
#    head=f'{home}{projname}'
#    binfile=f'{head}/{varbin}'
#    subprocess.call(f'/mnt/data/CaMaFlood/ECMWF/yrev_it {binfile} ./tmp.bin 1500 1320 {ihour}',shell=True)
#    varfp=open('./tmp.bin',"rb")
#    vardata=np.fromfile(varfp,dtype='<f',sep='',count=datasize).reshape(YSIZE,XSIZE)
#    ro_te0=ro_te[0,0,:,:]
#    xmask=vardata>999
#    vardata[xmask]=np.nan
#    ro_te0.data=vardata 
    clevels=leveldict[var]
#    fig=plt.figure(figsize=(8,5))
#    ax=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
#    ncfile=f'{dir_outnc}/{var}_{date}.nc'
#    xticks=123+np.arange(9)*3
#    yticks=24+np.arange(8)*3
#    ax.set_xticks(xticks,crs=ccrs.PlateCarree())
#    ax.set_yticks(yticks,crs=ccrs.PlateCarree())
#    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
        
#    ax.xaxis.set_major_formatter(lon_formatter)
#    ax.yaxis.set_major_formatter(lat_formatter)
        
#    ax.set_extent([123,148,24,46],crs=ccrs.PlateCarree())
#    ax.coastlines()
#    ax.gridlines(draw_labels=False)
    dt1=dt0
    for ihour in range(17):
        #
        fig=plt.figure(figsize=(8,5))
        ax=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
        ncfile=f'{dir_outnc}/{var}_{date}.nc'
        xticks=123+np.arange(9)*3
        yticks=24+np.arange(8)*3
        ax.set_xticks(xticks,crs=ccrs.PlateCarree())
        ax.set_yticks(yticks,crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        
        ax.set_extent([123,148,24,46],crs=ccrs.PlateCarree())
        ax.coastlines()
        ax.gridlines(draw_labels=False)
#
        ds=xr.open_dataset(ncfile)
        dsdata=ds[var]
        dsdata[ihour,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':f'{var}({unitdict[var]})'})
        date1=dt1.strftime("%Y%m%d%H")
        #        dstime=ds["time"]
        #       dstime=ds.variables["time"]
#        dstime_=ds.variables["time"]
        #        dstime_=dstime.dt.strftime("%Y-%m-%d %H:%M")
#        dstime1=dstime_[ihour]
        #        dstime1=dstime[ihour].strftime("%Y-%m-%d %H:%M")
#        dstime1_datetime = datetime.datetime.fromtimestamp(dstime1.astype(datetime.datetime) * 1e-9)
#        print(dstime1)
#        print(dstime1_datetime)
#        exit(0)
        title=f'{var} {date1}'
        ax.set_title(title)
        #ax.coastlines(resolution='10m')


        fig_title = f'{dir_outfig}/{var}{date1}.png'
        plt.savefig(fig_title)
        plt.close()
        dt1=dt1+datetime.timedelta(hours=1)

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        projname=args[1]
        date=args[2]        
        print(date)
    else:
        print('Arguments are too short')
        
