from pathlib import Path
import xarray
from matplotlib.pyplot import figure
import cartopy
import numpy as np
from dateutil.parser import parse
#import matplotlib.dates as mdates
from . import load
# WGS84 is the default, just calling it out explicity so somene doesn't wonder.
GREF = cartopy.crs.PlateCarree()#globe=cartopy.crs.Globe(ellipse='WGS84')

def overlay2d(img:xarray.DataArray):
    """plot NEXRAD reflectivity on map coordinates"""
    #hsv = rgb_to_hsv(d)

    ax = figure(figsize=(15,10)).gca(projection=GREF)

    ax.set_title(img.filename.name)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                  '50m',
                                  linestyle=':',linewidth=0.5, edgecolor='grey', facecolor='none'))

    labels = [[-117.1625, 32.715, 'San Diego'],
              [-87.9073, 41.9742, 'KORD' ],
              [-90.3755, 38.7503,'KSUS'],
              [-97.040443,32.897480,'KDFW'],
              [-104.6731667,39.8616667,'KDEN'],
              [ -111.1502604,45.7772358,'KBZN'],
              [ -106.6082622,35.0389316,'KABQ']
              ]
    if 0:
      for l in labels:
        ax.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
        ax.annotate(l[2], xy = (l[0], l[1]), xytext = (3, 3), textcoords = 'offset points')

    ax.imshow(img,origin='upper',
          extent=[img.lon[0], img.lon[-1], img.lat[0],img.lat[-1]],
          transform=GREF)


def keogram(flist:list, llslice:tuple, wld:Path):
    """ load all images from flist and stack a single lat or lon index"""
# %% generate slices
    try:
        ilat = float(llslice[0])
    except TypeError:
        ilat = None
    try:
        ilon = slice(float(llslice[1]))
    except ValueError:
        ilon = None

    if ilat is None and ilon is None:
        raise ValueError('must slice in lat or lon')
# %% setup arrays
    img = load(flist[0], wld, keo=False)
    coords = ('lat',img.lat) if ilon is not None else ('lon',img.lon)
    time = [parse(f.stem[6:]) for f in flist]

    keo = xarray.DataArray(np.empty((img.lon.size, len(flist), img.color.size),dtype=img.dtype),
                           coords=(coords,('time', time), ('color',img.color)))
# %% load and stack slices
    for f in flist:
        print(f,end='\r')
        img = load(f,wld, keo=False)
        if ilat is not None:
            keo.loc[:,img.time,:] = img.sel(lat=ilat, method='nearest', tolerance=0.1)
        elif ilon is not None:
            keo.loc[:,img.time,:] = img.sel(lon=ilon, method='nearest', tolerance=0.1)
# %%
    fg = figure(figsize=(15,10))
    ax = fg.gca()

    #tlim = mdates.date2num(keo.time[[0,-1]].values)
    #tlim = keo.time[[0,-1]].values
    #tlim = (None,None)
    tlim = (0,1)

    ax.imshow(keo.values,origin='upper', extent=[tlim[0], tlim[1], keo.lon[0].item(), keo.lon[-1].item()])
              #extent=[tlim[0],tlim[1], keo.lon[0].item(), keo.lon[-1].item()])

    fg.autofmt_xdate()
    ax.set_xlabel('Time [UTC]')
    ax.set_ylabel('Longitude [deg.]')
    ax.set_title(f'Keogram from lat={ilat}')

