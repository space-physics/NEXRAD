#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import show
#
import nexrad_quickplot as nq
import nexrad_quickplot.plots as nqp

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read')
    p.add_argument('pat',help='file glob pattern',nargs='?', default='*.png')
    p.add_argument('-wld',help='.wld filename',default='n0q.wld')
    p.add_argument('-k','--keo',help='make keogram',action='store_true')
    p = p.parse_args()
# %% find files to plot
    datadir = Path(p.datadir).expanduser()
    flist = [datadir] if datadir.is_file() else sorted(datadir.glob(p.pat))
# %% loop over all files
    for f in flist:
        img = nq.load(f, p.wld)
        if p.keo:
            nqp.keogram(img)
        else:
            nqp.overlay2d(img)

        show()
