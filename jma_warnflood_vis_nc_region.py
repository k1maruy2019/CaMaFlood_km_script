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
homenc='/usr/amoeba/pub/JMA_warnflood/nc/'
homefig='/usr/amoeba/pub/JMA_warnflood/fig/'
#projname=args[1]

#date=2022071906
date=args[1]
regionname=args[2]
ext_lon1=float(args[3])
ext_lon2=float(args[4])
ext_lat1=float(args[5])
ext_lat2=float(args[6])

#dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M%S")
dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M")
date=dt0.strftime("%Y%m%d%H%M")
print(date)

dir_nc=f'{homenc}'
#dir_nc=f'{homenc}{date}'
dir_outfig=f'{homefig}{regionname}/{date}'

os.makedirs(dir_outfig,exist_ok=True)

ihour=0
varlist=("warnflood",)
leveldict={}
leveldict["warnflood"]=(-1,0,1,2,3,4,5)
unitdict={}
unitdict["warnflood"]=""
titledict={}
titledict["warnflood"]="JMA_NOWCAS_WARN_INDEX_FLOOD"

for var in varlist:
    print(var)
    clevels=leveldict[var]
    title1=titledict[var]
    print(title1)
    dt1=dt0
    date1=dt1.strftime("%Y%m%d%H%M")
    for ihour in range(144):
        fig=plt.figure(figsize=(8,5))
        ax=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
        ncfile=f'{dir_nc}{date1}.nc'
        if not os.path.isfile(ncfile):
            continue
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
        dsdata[0,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':"INDEX"})
#        dsdata[ihour,:,:].plot.contourf(ax=ax,transform=ccrs.PlateCarree(), levels=clevels,cmap='rainbow',cbar_kwargs={'label':f'{var}({unitdict[var]})'})

        date1=dt1.strftime("%Y%m%d%H%M")

        title=f'{title1} {date1}'
        ax.set_title(title)

        fig_title = f'{dir_outfig}/{var}{date1}.png'
        plt.savefig(fig_title)
        plt.close()
        dt1=dt1+datetime.timedelta(minutes=10)
    subprocess.call(f'convert -delay 10 -loop 0 {dir_outfig}/{var}*.png {dir_outfig}/{var}.gif',shell=True)
    #convert -delay 5 -loop 0 outflw*.png outflw.gif
        
if __name__ == '__main__':
    args = sys.argv
    if 6 <= len(args):
#        projname=args[1]
        date=args[1]
        regionname=args[2]
        ext_lon1=args[3]
        ext_lon2=args[4]
        ext_lat1=args[5]
        ext_lat2=args[6]
        print(date)
    else:
        print('Arguments are too short')
        
