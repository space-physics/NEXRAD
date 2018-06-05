#!/usr/bin/env python
"""
keogram example:
python plot-nexrad.py ~/data/nexrad2017-08/temp/ --keo 40 none -odir ~/data/myplots
"""
from typing import Tuple, List, Optional
import nexrad_quickplot as nq
import nexrad_quickplot.plots as nqp
from pathlib import Path
from matplotlib.pyplot import show, pause
import seaborn as sns
sns.set_context('talk')


def nexrad_keogram(flist: List[Path], keo: List[str], wld: Path, odir: Path=None) -> Optional[Path]:

    keoreq: Tuple[str, float] = (keo[0], float(keo[1]))

    ofn = odir / f'keo-{keo[0]}{keo[1]}-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
    keo = nq.keogram(flist, keoreq, wld)

    nqp.keogram(keo, ofn)

    return ofn


def nexrad_loop(flist: List[Path], wld: Path, odir: Path):
    mlp = None
    for f in flist:
        ofn = odir / ('map'+f.name[6:]) if odir else None
        img = nq.load(f, P.wld)
        mlp = nqp.overlay2d(img, ofn, mlp)
        if not ofn:  # display only
            pause(1)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir', help='directory of NEXRAD PNG data to read', nargs='+')
    p.add_argument('-pat', help='file glob pattern', nargs='?', default='*.png')
    p.add_argument('-wld', help='.wld filename', default='n0q.wld')
    p.add_argument('-keo', help='make keogram at lat/lon value',
                   metavar=('lat/lon', 'value'), nargs=2)
    p.add_argument('-odir', help='save graphs to this directory')
    p.add_argument
    P = p.parse_args()

    odir = Path(P.odir).expanduser() if P.odir else None
# %% find files to plot
    if len(P.datadir) > 1:
        flist = [Path(f).expanduser() for f in P.datadir if f.is_file()]
    else:
        datadir = Path(P.datadir[0]).expanduser()
        flist = [datadir] if datadir.is_file() else sorted(datadir.glob(P.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'did not find files in {datadir} with pattern {P.pat}')
# %% Process / Plot
    if P.keo is not None:
        ofn = nexrad_keogram(flist, P.keo, P.wld, odir)
        print('keogram created at', ofn)
    else:  # full image plots
        nexrad_loop(flist, P.wld, odir)
        if odir:
            print('\nImageMagick can convert the PNGs to animated GIF by a command like:')
            print(f'\nconvert map2018-0101T09*.png out.gif')
    show()
