#!/usr/bin/env python
"""
keogram example:
python plot-nexrad.py ~/data/2017-08-21/nexrad/ -keo lat 40 -odir ~/data/myplots

Plot stack example:
./plot-nexrad.py ~/data/2017-08-21/nexrad/ -odir ~/data/2017-08-21/nexrad/plots -pat nexrad2017-08-21T14*.png

Panel subplot example:
./plot-nexrad.py ~/data/2017-08-21/nexrad/nexrad2017-08-21T12:00:00.png ~/data/2017-08-21/nexrad/nexrad2017-08-21T12:30:00.png -odir ~/data/2017-08-21/nexrad/plots
"""
from pathlib import Path
from argparse import ArgumentParser
from matplotlib.pyplot import show
import nexradutils.plots as nqp


SCALEFN = Path(__file__).parent / 'doc' / 'n0q_ramp.png'


def main():
    p = ArgumentParser()
    p.add_argument('datadir', help='directory of NEXRAD PNG data to read', nargs='+')
    p.add_argument('-pat', help='file glob pattern', nargs='?', default='*.png')
    p.add_argument('-wld', help='.wld filename')
    p.add_argument('-keo', help='make keogram at lat/lon value',
                   metavar=('lat/lon', 'value'), nargs=2)
    p.add_argument('-lattick', help='specify specific latitude to have additional tick at',
                   type=float)
    p.add_argument('-odir', help='save graphs to this directory')
    p.add_argument('-q', '--quiet', help='no plots', action='store_true')
    p.add_argument
    P = p.parse_args()

    nqp.genplots(P, SCALEFN)

    if show is not None:
        show()


if __name__ == '__main__':
    main()
