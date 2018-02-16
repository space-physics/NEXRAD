#!/usr/bin/env python
from pathlib import Path
from datetime import datetime,timedelta
import urllib.request
import numpy as np


def wld2mesh(fn:Path, nxy:tuple) -> np.ndarray:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
    wld = np.loadtxt(fn)

    ny, nx = nxy

    lat = np.arange(wld[5]-wld[3] + ny*wld[3], wld[5]-wld[3], -wld[3])
    lon = np.arange(wld[4], wld[4]+nx*wld[0], wld[0])

    return lat, lon


def datetimerange(start:datetime, stop:datetime, step:timedelta) -> list:
    return [start + i*step for i in range((stop-start) // step)]


def get_goes(t:datetime, outdir:Path, goes:int, mode:str):
    """download GOES file for this time
    https://www.ncdc.noaa.gov/gibbs/image/GOE-13/IR/2017-08-21-06
    """
    STEM = 'https://www.ncdc.noaa.gov/gibbs/image/GOE-'

    dgoes = f'{t.year}-{t.month:02d}-{t.day:02d}-{t.hour:02d}'

    fn = outdir / f"goes{goes:d}-{mode}-{dgoes}.jpg"

    if fn.is_file(): # no clobber
        return

    url = (f'{STEM}{goes}/{mode}/' + dgoes)

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)


def get_nexrad(t:datetime, outdir:Path):
    """download NEXRAD file for this time
    https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
    """
    STEM = 'https://mesonet.agron.iastate.edu/archive/data/'

    fn = outdir/f"nexrad{t.isoformat()}.png"

    if fn.is_file(): # no clobber
        return

    url = (f'{STEM}{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png')

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)