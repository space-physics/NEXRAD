#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import show
#
import nexrad_quickplot as nq
from nexrad_quickplot.plots import plotnexrad

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read')
    p.add_argument('pat',help='file glob pattern',nargs='?', default='*.png')
    p.add_argument('-wld',help='.wld filename',default='n0q.wld')
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()
    if datadir.is_file():
        flist = [datadir]
    else:
        flist = sorted(datadir.glob(p.pat))

    img = nq.loadnexrad(flist[0])
    lat, lon = nq.wld2mesh(p.wld, img.shape[:2])


    for f in flist:
        img = nq.loadnexrad(f)
        plotnexrad(img, f, lat, lon)
        show()
