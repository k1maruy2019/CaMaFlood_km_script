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
regionname=args[3]
ext_lon1=float(args[4])
ext_lon2=float(args[5])
ext_lat1=float(args[6])
ext_lat2=float(args[7])

#dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M%S")
dt0=datetime.datetime.strptime(date,"%Y%m%d%H")
date=dt0.strftime("%Y%m%d%H")
print(date)

dir_outnc=f'{homenc}{projname}/{date}'
dir_outfig=f'{homefig}{projname}_{regionname}/{date}'

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
    clevels=leveldict[var]
    dt1=dt0
    for ihour in range(17):
        #
        fig=plt.figure(figsize=(8,5))
        ax=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
        ncfile=f'{dir_outnc}/{var}_{date}.nc'
#        xticks=123+np.arange(9)*3
#        yticks=24+np.arange(8)*3
        xticks=123+np.arange(27)
        yticks=24+np.arange(24)
        ax.set_xticks(xticks,crs=ccrs.PlateCarree())
        ax.set_yticks(yticks,crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        
        ax.set_extent([ext_lon1,ext_lon2,ext_lat1,ext_lat2],crs=ccrs.PlateCarree())
        ax.coastlines()
        ax.gridlines(draw_labels=False)
        
        ds=xr.open_dataset(ncfile)
        dsdata=ds[var]
        dsdata[ihour,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':f'{var}({unitdict[var]})'})
        date1=dt1.strftime("%Y%m%d%H")

        title=f'{var} {date1}'
        ax.set_title(title)

        fig_title = f'{dir_outfig}/{var}{date1}.png'
        plt.savefig(fig_title)
        plt.close()
        dt1=dt1+datetime.timedelta(hours=1)
    subprocess.call(f'convert -delay 5 -loop 0 {dir_outfig}/{var}*.png {dir_outfig}/{var}.gif',shell=True)
    #convert -delay 5 -loop 0 outflw*.png outflw.gif
        
if __name__ == '__main__':
    args = sys.argv
    if 7 <= len(args):
        projname=args[1]
        date=args[2]
        regionname=args[3]
        ext_lon1=args[4]
        ext_lon2=args[5]
        ext_lat1=args[6]
        ext_lat2=args[7]
        print(date)
    else:
        print('Arguments are too short')
        
