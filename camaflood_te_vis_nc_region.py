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
##
# for TE
homenc='/usr/amoeba/pub/CaMaFlood/TE/data'
homefig='/usr/amoeba/pub/CaMaFlood/outfig/'
# for TE
##
#projname="test3-jpn_fcast_EC/"
projname=args[1]
#date=2022071906
date=args[2]
regionname=args[3]
ext_lon1=float(args[4])
ext_lon2=float(args[5])
ext_lat1=float(args[6])
print(ext_lat1)
ext_lat2=float(args[7])


# for TE
dir_outnc=f'{homenc}/{date}'
dir_outfig=f'{homefig}/{projname}_{regionname}/TE/{date}'
# for TE

os.makedirs(dir_outfig,exist_ok=True)

ihour=0
varlist=("runoff","gprct")
leveldict={}
leveldict["runoff"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
leveldict["gprct"]=(0,0.1,0.3,0.5,1,3,5,7,10,15)
unitdict={}
unitdict["runoff"]="kg/m2/s"
unitdict["gprct"]="kg/m2/s"

#dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M%S")
dt0=datetime.datetime.strptime(date,"%Y%m%d")
date=dt0.strftime("%Y%m%d")
print(date)

for var in varlist:
    clevels=leveldict[var]
    dt1=dt0
    for ihour in range(24):
        #
        fig=plt.figure(figsize=(8,5))
        ax=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
# for TE
       # "TE-JPN01M_MSM_H2022071212_RUNOFF.nc"
       # "TE-JPN01M_MSM_H2022071212_GPRCT.nc"
        upp_var=var.upper()
        hour=str(ihour).zfill(2)
        ncfile=f'{dir_outnc}/{upp_var}/TE-JPN01M_MSM_H{date}{hour}_{upp_var}.nc'
# for TE
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
##  for TE
        dsdata=ds[upp_var]*1000
        dsdata[0,0,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':f'{var}({unitdict[var]})'})
#        dsdata[ihour,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':f'{var}({unitdict[var]})'})        
##  for TE               
        date1=dt1.strftime("%Y%m%d")

        title=f'{var} {date1}_{hour}'
        ax.set_title(title)

        os.makedirs(f'{dir_outfig}/{upp_var}',exist_ok=True)
        fig_title = f'{dir_outfig}/{upp_var}/{var}_{date1}{hour}.png'
        plt.savefig(fig_title)
        plt.close()
        dt1=dt1+datetime.timedelta(hours=1)
    subprocess.call(f'convert -delay 5 -loop 0 {dir_outfig}/{upp_var}/{var}*.png {dir_outfig}/{upp_var}/{var}_{date}.gif',shell=True)
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
        
