#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import show
#
import nexrad_quickplot as nq
import nexrad_quickplot.plots as nqp

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read',nargs='+')
    p.add_argument('-pat',help='file glob pattern',nargs='?', default='*.png')
    p.add_argument('-wld',help='.wld filename',default='n0q.wld')
    p.add_argument('-k','--keo',help='make keogram at lat,lon  (none for no cut)',nargs=2)
    p = p.parse_args()
# %% find files to plot
    if len(p.datadir) > 1:
        flist = [Path(f).expanduser() for f in p.datadir]
    else:
        datadir = Path(p.datadir[0]).expanduser()
        flist = [datadir] if datadir.is_file() else sorted(datadir.glob(p.pat))
#%% keogram
    if p.keo is not None:
        nqp.keogram(flist, p.keo, p.wld)
        show()
# %% loop over all files
    for f in flist:
        img = nq.load(f, p.wld)
        nqp.overlay2d(img)

        show()
