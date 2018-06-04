#!/usr/bin/env python
"""
keogram example:
python plot-nexrad.py ~/data/nexrad2017-08/temp/ --keo 40 none -odir ~/data/myplots
"""
import nexrad_quickplot as nq
import nexrad_quickplot.plots as nqp
from pathlib import Path
from matplotlib.pyplot import show
import seaborn as sns
sns.set_context('talk')


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir', help='directory of NEXRAD PNG data to read', nargs='+')
    p.add_argument('-pat', help='file glob pattern', nargs='?', default='*.png')
    p.add_argument('-wld', help='.wld filename', default='n0q.wld')
    p.add_argument('-k', '--keo', help='make keogram at lat,lon  (none for no cut)',
                   metavar=('lat', 'lon'), nargs=2, type=float)
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
# %% keogram
    if P.keo is not None:
        ofn = odir / f'keo-lat{P.keo[0]}-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
        nqp.keogram(flist, P.keo, P.wld, ofn)
    else:
        # %% loop over all files
        mlp = None
        for f in flist:
            ofn = odir / ('map'+f.name[6:]) if odir else None
            img = nq.load(f, P.wld)
            mlp = nqp.overlay2d(img, ofn, mlp)

    show()
