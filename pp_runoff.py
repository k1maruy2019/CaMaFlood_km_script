#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

import sys
import os

argvs=sys.argv
argc=len(argvs)

if( argc != 4):
    print('Usage: %s date hour1 hour2',argvs[0])
    quit()
date = argvs[1];
hour1 = argvs[2];
hour2 = argvs[3];
print(f'date={date}')
print(f'hour1={hour1}')
print(f'hour2={hour2}')

file1= f'/usr/amoeba/pub/CaMaFlood/ECMWF.free/{date}/RUNOFF/ro_{date}_00z_{hour1}_jpn.nc'
data1 = xr.open_dataset(file1)
file2= f'/usr/amoeba/pub/CaMaFlood/ECMWF.free/{date}/RUNOFF/ro_{date}_00z_{hour2}_jpn.nc'
data2 = xr.open_dataset(file2)

ro1=data1["var2_0_201_surface"]
ro2=data2["var2_0_201_surface"]
ro1=ro1*1000
ro1_mean=ro1.mean(dim=("longitude","latitude"))
ro2=ro2*1000
ro2_mean=ro2.mean(dim=("longitude","latitude"))
ro3=ro2
tmp=ro2.data-ro1.data

from array import array
import subprocess
data=array('f',tmp.flatten())
f=open('tmp.bin','wb')
f.write(data)
f.close()
os.chdir('/usr/amoeba/pub/CaMaFlood/script') 
subprocess.call('./yrev_downscale ./tmp.bin ./tmp_rev_downscale.bin',shell=True)

XSIZE=1500
YSIZE=1320
datasize4=XSIZE*YSIZE*4
datasize=XSIZE*YSIZE
subprocess.call('./yrev tmp_rev_downscale.bin tmp_rev_downscale_rev.bin 1500 1320',shell=True)
binfile=open("tmp_rev_downscale_rev.bin","rb")
array0=np.fromfile(binfile,dtype='<f',sep='',count=datasize).reshape(YSIZE,XSIZE)
#data=array('f',mask.flatten())
#f=open('mask_TE_JPN.bin','wb')
#f.write(data)
#f.close()
binfile=open("mask_TE_JPN.bin","rb")
mask=np.fromfile(binfile,dtype='<f',sep='',count=datasize).reshape(YSIZE,XSIZE)
array1=array0*mask
data=array('f',array1.flatten())
f=open('masked.bin','wb')
f.write(data)
f.close()
subprocess.call('/usr/amoeba/pub/CaMaFlood/script/yrev masked.bin masked_rev.bin 1500 1320',shell=True)
subprocess.call('rm tmp.bin masked.bin tmp_rev_downscale.bin tmp_rev_downscale_rev.bin',shell=True)



