from pathlib import Path
import xarray
import numpy as np
import bisect
import imageio
import logging
from typing import Dict, Any, Union, List, Optional
from matplotlib.pyplot import figure, draw, fignum_exists, pause
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

from . import load
from .io import loadkeogram
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# WGS84 is the default, just calling it out explicity so somene doesn't wonder.
GREF = cartopy.crs.PlateCarree()  # globe=cartopy.crs.Globe(ellipse='WGS84')


labels = [[-117.1625, 32.715, 'San Diego'],
          [-87.9073, 41.9742, 'KORD'],
          [-90.3755, 38.7503, 'KSUS'],
          [-97.040443, 32.897480, 'KDFW'],
          [-104.6731667, 39.8616667, 'KDEN'],
          [-111.1502604, 45.7772358, 'KBZN'],
          [-106.6082622, 35.0389316, 'KABQ']
          ]

LAT_TICK = list(range(20, 55, 5))
LON_TICK = list(range(-140, -40, 20))
DPI = 600


def nexrad_panel(flist: List[Path],
                 wld: Path, ofn: Optional[Path],
                 lattick: float=None,
                 scalefn: Path=None):
    if figure is None:
        logging.error('skipping panel plot')
        return

    fg = figure()
    axs = fg.subplots(len(flist), 1, sharex=True, subplot_kw=dict(projection=GREF))

    mlp = {'fg': fg}
    xlabel: List[bool] = [False] * len(flist)
    xlabel[-1] = True
    for ax, fn, xlb in zip(axs, flist, xlabel):
        mlp['ax'] = ax
        mlp['himg'] = None
        mlp['xlabel'] = xlb

        mlp = overlay2d(load(fn, wld), mlp=mlp, lattick=lattick)

    fg.suptitle('NEXRAD N0Q reflectivity')
# %% color scale
    if scalefn and scalefn.is_file():
        scale = np.rot90(imageio.imread(scalefn), 2)
        ax = fg.add_axes([0.85, 0.25, 0.075, 0.5])
        ax.imshow(scale)
        ax.axis('off')  # turn off all ticks, etc.
# %% optional plot save
    if ofn:
        print('saving', ofn)
        fg.savefig(ofn, bbox_inches='tight', dpi=DPI)


def overlay2d(img: xarray.DataArray,
              ofn: Path=None,
              mlp: Dict[str, Any]={},
              lattick: Union[float, int, list]=None,
              lontick: Union[float, int, list]=None,
              scalefn: Path=None,
              verbose: bool=False) -> dict:
    """plot NEXRAD reflectivity on map coordinates"""
    if figure is None:
        logging.error('skipping overlay plot')
        return {}

    title = img.filename.stem[6:-3]

    def _savemap(ofn, fg):
        if ofn is not None:
            ofn = Path(ofn).expanduser()
            print('saving Nexrad map:', ofn, end='\r')
            fg.savefig(ofn, bbox_inches='tight', dpi=DPI)

    if 'fg' in mlp and fignum_exists(mlp['fg'].number) and 'himg' in mlp and mlp['himg'] is not None:
        mlp['himg'].set_data(img)
        mlp['ht'].set_text(title)
        draw()
        _savemap(ofn, mlp['fg'])
        return mlp
# %% make new figure
    if 'ax' not in mlp:
        fg = figure(figsize=(15, 10))
        ax = fg.gca(projection=GREF)
    else:
        fg = mlp['fg']
        ax = mlp['ax']

    ht = ax.set_title(title)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                                       '50m',
                                                       linestyle=':', linewidth=0.5, edgecolor='grey', facecolor='none'))

    if verbose:
        for l in labels:
            ax.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
            ax.annotate(l[2], xy=(l[0], l[1]), xytext=(3, 3), textcoords='offset points')

    himg = ax.imshow(img, origin='upper',
                     extent=[img.lon[0], img.lon[-1], img.lat[0], img.lat[-1]],
                     transform=GREF)
# %% grid lines and labels
    gl = ax.gridlines(crs=GREF, draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, linestyle='--')

    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right = False
    if 'xlabel' in mlp and not mlp['xlabel']:
        gl.xlabels_bottom = False

    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
# %% ticks
    if isinstance(lontick, (int, float)):
        bisect.insort(LON_TICK, lontick)
        lontick = LON_TICK
    elif lontick is None:
        lontick = LON_TICK

    if isinstance(lattick, (int, float)):
        bisect.insort(LAT_TICK, lattick)
        lattick = LAT_TICK
    elif lattick is None:
        lattick = LAT_TICK

    gl.xlocator = mticker.FixedLocator(lontick)
    gl.ylocator = mticker.FixedLocator(lattick)

    draw()
    _savemap(ofn, fg)

    mlp = {'fg': fg, 'ax': ax, 'himg': himg, 'ht': ht}

    return mlp


def keogram(keo: xarray.DataArray,
            ofn: Path=None,
            scalefn: Path=None):
    """stack a single lat or lon index"""
    if figure is None:
        logging.error('skipping keogram')
        return
# %%
    fg = figure(figsize=(15, 10))
    ax = fg.gca()

    tlim = mdates.date2num(keo.time[[0, -1]].values)

    ax.imshow(keo.values, origin='upper',
              aspect='auto',  # crucial for time-based imshow()
              extent=[tlim[0], tlim[1], keo.lon[0].item(), keo.lon[-1].item()])

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fg.autofmt_xdate()

    ax.set_xlabel('Time [UTC]')
    ax.set_ylabel('Longitude [deg.]')
    ax.set_title(f'NEXRAD Keogram: cut at lat={keo.lat}\n'
                 f'{keo.time.values[0]} to {keo.time.values[-1]}')

    draw()
# %%
    if ofn is not None:
        ofn = Path(ofn).expanduser()
        print('saving keogram to', ofn)
        fg.savefig(ofn, bbox_inches='tight', dpi=DPI)


def genplots(P, scalefn: Path, quiet: bool=False):

    odir = Path(P.odir).expanduser() if P.odir else None
# %% file list--panel
    if len(P.datadir) > 1:
        flist = [Path(f).expanduser() for f in P.datadir]
        ofn = odir / f'panel-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
        if not quiet:
            nexrad_panel(flist, P.wld, ofn, P.lattick, scalefn=scalefn)
        return
# %% glob input directory
    datadir = Path(P.datadir[0]).expanduser()
    flist = [datadir] if datadir.is_file() else sorted(datadir.glob(P.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'did not find files in {datadir} with pattern {P.pat}')
# %% Process / Plot
    if isinstance(P.keo, list) and len(P.keo) == 2:
        ofn = nexrad_keogram(flist, P.keo, P.wld, odir, scalefn=scalefn, quiet=P.quiet)
        print('keogram created at', ofn)
    else:
        nexrad_loop(flist, P.wld, odir, P.lattick, scalefn=scalefn, quiet=P.quiet)
        if odir:
            print('\nImageMagick can convert the PNGs to animated GIF by a command like:')
            print('\nconvert map2018-0101T09*.png out.gif')


def nexrad_keogram(flist: List[Path], keo: List[str],
                   wld: Path, odir: Path=None, scalefn: Path=None, quiet: bool=False) -> Optional[Path]:

    keoreq = (keo[0], float(keo[1]))

    ofn = odir / f'keo-{keo[0]}{keo[1]}-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
    dkeo = loadkeogram(flist, keoreq, wld)

    if not quiet:
        keogram(dkeo, ofn, scalefn=scalefn)

    return ofn


def nexrad_loop(flist: List[Path],
                wld: Path, odir: Optional[Path],
                lattick: float=None, scalefn: Path=None, quiet: bool=False):

    mlp: dict = {}
    for f in flist:
        ofn = odir / ('map' + f.name[6:]) if odir else None
        img = load(f, wld)
        if not quiet:
            mlp = overlay2d(img, ofn, mlp, lattick=lattick, scalefn=scalefn)
            if not ofn:  # display only
                pause(1)
