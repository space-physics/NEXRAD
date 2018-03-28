#!/usr/bin/env python
"""
keogram example:
python plot-nexrad.py ~/data/nexrad2017-08/temp/ --keo 40 none -odir ~/data/myplots


"""
from pathlib import Path
from matplotlib.pyplot import show
import seaborn as sns
sns.set_context('talk')
#
import nexrad_quickplot as nq
import nexrad_quickplot.plots as nqp

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read',nargs='+')
    p.add_argument('-pat',help='file glob pattern',nargs='?', default='*.png')
    p.add_argument('-wld',help='.wld filename',default='n0q.wld')
    p.add_argument('-k','--keo',help='make keogram at lat,lon  (none for no cut)',metavar=('lat','lon'),nargs=2)
    p.add_argument('-odir',help='save graphs to this directory')
    p.add_argument
    p = p.parse_args()

    odir = Path(p.odir).expanduser() if p.odir else None
# %% find files to plot
    if len(p.datadir) > 1:
        flist = [Path(f).expanduser() for f in p.datadir if f.is_file()]
    else:
        datadir = Path(p.datadir[0]).expanduser()
        flist = [datadir] if datadir.is_file() else sorted(datadir.glob(p.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'did not find files in {datadir} with pattern {p.pat}')
#%% keogram
    if p.keo is not None:
        ofn = odir / f'keo-lat{p.keo[0]}-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
        nqp.keogram(flist, p.keo, p.wld, ofn)
    else:
# %% loop over all files
        mlp = None
        for f in flist:
            ofn = odir / ('map'+f.name[6:]) if odir else None
            img = nq.load(f, p.wld)
            mlp = nqp.overlay2d(img, ofn, mlp)

    show()