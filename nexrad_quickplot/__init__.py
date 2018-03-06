#!/usr/bin/env python
from pathlib import Path
from datetime import datetime,timedelta
import urllib.request
import skimage.transform
import numpy as np
import imageio


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


def get_nexrad(t:datetime, outdir:Path):
    """download NEXRAD file for this time
    https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
    """
    STEM = 'https://mesonet.agron.iastate.edu/archive/data/'
    outdir = Path(outdir).expanduser()

    fn = outdir/f"nexrad{t.isoformat()}.png"

    if fn.is_file(): # no clobber
        return

    url = (f'{STEM}{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png')

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)


def loadnexrad(fn:Path, downsample:int=None):
    """
    loads and modifies NEXRAD image for plotting
    """

    img = imageio.imread(str(fn))

    assert img.ndim==3 and img.shape[2] == 4,'unexpected NEXRAD image format'

    if downsample is not None:
        img = skimage.transform.resize(img, (img.shape[0]//downsample, img.shape[1]//downsample),
                                   mode='constant',cval=255,
                                    preserve_range=True).astype(img.dtype)
    # make transparent (arbitrary)
    img[...,-1] = 128

    mask = img[...,:3].all(axis=2) == 0
    img[mask,:3] = 255  # make no signal be white

    return img
