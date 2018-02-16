#!/usr/bin/env python
from pathlib import Path
import numpy as np
from scipy.misc import imread
from matplotlib.pyplot import figure,draw,pause
from matplotlib.colors import rgb_to_hsv
#from metpy.plots import ctables

#def extract_colormap():
#    norm, cmap = ctables.registry.get_with_steps('NWSReflectivity', -75, 0.5)
#    rgb = cmap(np.arange(16))

#    return rgb


def loaddata(datadir:Path, pat:str='*.png', N:int=1):


    datadir = Path(datadir).expanduser()

    flist = datadir.glob(pat)
    for _ in range(N):
        fn = next(flist)
        rgb = imread(str(fn))
        hsv = rgb_to_hsv(rgb)

        if 1:
            ax = figure().gca()
            ax.imshow(rgb)
            ax.set_title(fn.name)

        ax = figure().gca()
        ax.hist(hsv.ravel(), bins=64)
        ax.set_yscale('log')

        if 0:
            ax = figure().gca()
            ax.imshow(hsv, cmap='hsv')
            ax.set_title(fn.name)

        draw()
        pause(0.001)

    return rgb


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read')
    p.add_argument('pat',help='file glob pattern',nargs='?'
    p.add_argument('-N',help='number of images to process',type=int,default=1)
    p = p.parse_args()

    rgb = loaddata(p.datadir, p.pat, p.N)

