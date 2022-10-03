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
import shutil
import datetime

import subprocess

args=sys.argv
homenc='/usr/amoeba/pub/JMA_warnflood/nc/'
homefig='/usr/amoeba/pub/JMA_warnflood/fig/'
#projname=args[1]

#date=2022071906
date=args[1]
tenminutes=int(args[2])
regionname=args[3]
#ext_lon1=float(args[3])
#ext_lon2=float(args[4])
#ext_lat1=float(args[5])
#ext_lat2=float(args[6])

dt0=datetime.datetime.strptime(date,"%Y%m%d%H%M%S")
date=dt0.strftime("%Y%m%d%H%M")
print(date)

dir_nc=f'{homenc}'


#os.makedirs(dir_outfig,exist_ok=True)

ihour=0
varlist=("warnflood",)

tempdir=f'{homefig}temp/'
os.makedirs(tempdir,exist_ok=True)
for var in varlist:
    dt1=dt0
    date1=dt1.strftime("%Y%m%d%H%M")
    for itenminute in range(tenminutes):
        date0=dt1.strftime("%Y%m%d0000")
        dir_outfig=f'{homefig}{regionname}/{date0}'
        fig_title = f'{dir_outfig}/{var}{date1}.png'
#        print(f'{fig_title}')
#        print(f'{tempdir}{var}{date1}.png')
        shutil.copy2(f'{fig_title}',f'{tempdir}{var}{date1}.png')
        dt1=dt1+datetime.timedelta(minutes=10)
        date1=dt1.strftime("%Y%m%d%H%M")
    subprocess.call(f'convert -delay 10 -loop 0 {tempdir}*.png {homefig}{regionname}/{var}{date}_{tenminutes}.gif',shell=True)
    #convert -delay 5 -loop 0 outflw*.png outflw.gif # 1hour 5 is too fast
    # 10minites -delay 10 OK                  
os.remove(f'{tempdir}*.png')
                     
if __name__ == '__main__':
    args = sys.argv
    if 3 <= len(args):
#        projname=args[1]
        date=args[1]
        tenminutes=int(args[2])
        regionname=args[3]
    else:
        print('Arguments are too short')

        
