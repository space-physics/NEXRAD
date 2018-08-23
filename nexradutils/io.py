import imageio
from pathlib import Path
import xarray
import logging
import functools
from dateutil.parser import parse
import numpy as np
from datetime import datetime, date, time
import os
import requests
from typing import Sequence, Tuple
try:
    import skimage.transform as st
except ImportError:
    st = None

R = Path(__file__).parent
WLD = R / 'data' / 'n0q.wld'


def download(t: datetime, outdir: Path, overwrite: bool=False) -> Path:
    """download NEXRAD file for this time
    https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
    """
    STEM = 'https://mesonet.agron.iastate.edu/archive/data/'
    outdir = Path(outdir).expanduser()

    if isinstance(t, date) and not isinstance(t, datetime):
        t = datetime.combine(t, time.min)

    if os.name == 'nt':
        fn = outdir / f"nexrad{t.isoformat().replace(':','-')}.png"
    else:
        fn = outdir / f"nexrad{t.isoformat()}.png"
# %%
    url: str = (f'{STEM}{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_'
                f'{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png')

    urlretrieve(url, fn, overwrite)

    return fn


def load(fn: Path, wld: Path=None, downsample: int=None, keo: bool=False) -> xarray.DataArray:
    """
    loads and modifies NEXRAD image for plotting
    """
    fn = Path(fn).expanduser()

    img = imageio.imread(fn)

    assert img.ndim == 3 and img.shape[2] in (3, 4), 'unexpected NEXRAD image format'

    if downsample is not None:
        assert isinstance(downsample, int)
        if st is None:
            raise ImportError('install scikit-image by: \n  pip install skimage')
        img = st.downscale_local_mean(img, (downsample, downsample, 1), cval=255).astype(img.dtype)

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


def urlretrieve(url: str, fn: Path, overwrite: bool=False):
    if not overwrite and fn.is_file() and fn.stat().st_size > 10000:
        print(f'SKIPPED {fn}')
        return
# %% prepare to download
    R = requests.head(url, allow_redirects=True, timeout=10)
    if R.status_code != 200:
        logging.error(f'{url} not found. \n HTTP ERROR {R.status_code}')
        return
# %% download
    print(f'downloading {int(R.headers["Content-Length"])//1000000} MBytes:  {fn.name}')
    R = requests.get(url, allow_redirects=True, timeout=10)
    with fn.open('wb') as f:
        f.write(R.content)


@functools.lru_cache()
def wld2mesh(wldfn: Path, nxy: tuple) -> np.ndarray:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
    if not wldfn:
        wldfn = WLD

    wld = np.loadtxt(wldfn)

    # ny, nx = nxy
    ny, nx = (5400, 12200)  # FIXME has to be from original image size

    lat = np.linspace(wld[5] + ny * wld[3], wld[5], nxy[0])
    lon = np.linspace(wld[4], wld[4] + nx * wld[0], nxy[1])
    # trailing index fixes occasional off by one due to floating point error
    # lat = np.arange(wld[5]-wld[3] + ny*wld[3], wld[5]-wld[3], -wld[3])[:ny]
    # lon = np.arange(wld[4], wld[4]+nx*wld[0], wld[0])[:nx]

    return lat, lon


def loadkeogram(flist: Sequence[Path], llslice: Tuple[str, float], wld: Path=None) -> xarray.DataArray:
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
