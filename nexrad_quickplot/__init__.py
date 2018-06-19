#!/usr/bin/env python
import os
from pathlib import Path
from typing import List, Tuple
from datetime import datetime, timedelta
from dateutil.parser import parse
import urllib.request
import numpy as np
import xarray
import imageio
import functools
try:
    import skimage.transform as st
except ImportError:
    st = None


@functools.lru_cache()
def wld2mesh(fn: Path, nxy: tuple) -> np.ndarray:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
    wld = np.loadtxt(fn)

    # ny, nx = nxy
    ny, nx = (5400, 12200)  # FIXME has to be from original image size

    lat = np.linspace(wld[5] + ny * wld[3], wld[5], nxy[0])
    lon = np.linspace(wld[4], wld[4] + nx * wld[0], nxy[1])
    # trailing index fixes occasional off by one due to floating point error
    # lat = np.arange(wld[5]-wld[3] + ny*wld[3], wld[5]-wld[3], -wld[3])[:ny]
    # lon = np.arange(wld[4], wld[4]+nx*wld[0], wld[0])[:nx]

    return lat, lon


def datetimerange(start: datetime, stop: datetime, step: timedelta) -> List[datetime]:
    return [start + i * step for i in range((stop - start) // step)]


def download(t: datetime, outdir: os.PathLike, clobber: bool=False) -> Path:
    """download NEXRAD file for this time
    https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
    """
    STEM = 'https://mesonet.agron.iastate.edu/archive/data/'
    outdir = Path(outdir).expanduser()

    if os.name == 'nt':
        fn = outdir / f"nexrad{t.isoformat().replace(':','-')}.png"
    else:
        fn = outdir / f"nexrad{t.isoformat()}.png"
# %%
    if not clobber and fn.is_file():  # no clobber
        print(fn, 'SKIPPED', end='\r')
        return fn

    url: str = (f'{STEM}{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_'
                f'{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png')

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)

    return fn


def load(fn: Path, wld: Path, downsample: int=None, keo: bool=False) -> xarray.DataArray:
    """
    loads and modifies NEXRAD image for plotting
    """
    if not fn.is_file():
        raise FileNotFoundError(f'{fn} is not a file.')

    img = imageio.imread(fn)

    assert img.ndim == 3 and img.shape[2] in (3, 4), 'unexpected NEXRAD image format'

    if downsample is not None:
        assert isinstance(downsample, int)
        if st is None:
            raise ImportError('you need to install scikit-image    pip install skimage')
        img = st.resize(img, (img.shape[0] // downsample, img.shape[1] // downsample),
                        mode='constant', cval=255,
                        preserve_range=True).astype(img.dtype)

# %% make transparent
    if not keo:
        img = img[..., :3]

        mask = img[..., :3].all(axis=2) == 0
        img[mask, :3] = 255  # make no signal be white

# %% collect output
    lat, lon = wld2mesh(wld, img.shape[:2])

    img = xarray.DataArray(img,
                           coords=[('lat', lat), ('lon', lon), ('color', ['R', 'G', 'B'])],
                           attrs={'filename': fn, 'wldfn': wld, 'time': parse(fn.stem[6:])})

    assert img.dtype in (np.uint8, np.uint16)

    return img


def keogram(flist: List[Path], llslice: Tuple[str, float], wld: Path) -> xarray.DataArray:
    # %% generate slices
    ilat = None
    ilon = None
    if llslice[0] == 'lat':
        ilat = llslice[1]
    elif llslice[0] == 'lon':
        ilon = llslice[1]
    else:
        raise ValueError(f'unknown keogram slice {llslice}')

    if ilat is None and ilon is None:
        raise ValueError('must slice in lat or lon')

    assert ilat is not None, 'FIXME: currently handling latitude cut (longitude keogram) only'
# %% setup arrays
    img = load(flist[0], wld, keo=False)
    coords = ('lat', img.lat) if ilon is not None else ('lon', img.lon)
    time = [parse(f.stem[6:]) for f in flist]

    keo = xarray.DataArray(np.empty((img.lon.size, len(flist), img.color.size), dtype=img.dtype),
                           coords=(coords, ('time', time), ('color', img.color)))
# %% load and stack slices
    for f in flist:
        print(f, end='\r')
        img = load(f, wld, keo=False)
        if ilat is not None:
            keo.loc[:, img.time, :] = img.sel(lat=ilat, method='nearest', tolerance=0.1)
            keo.attrs['lat'] = ilat
        elif ilon is not None:
            keo.loc[:, img.time, :] = img.sel(lon=ilon, method='nearest', tolerance=0.1)
            keo.attrs['lon'] = ilon

    return keo
