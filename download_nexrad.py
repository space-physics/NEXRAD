#!/usr/bin/env python
"""parallel file downloading for Python 3

to downsize these images en masse, see
https://www.scivision.co/force-imagemagick-ram-drive/
"""
from datetime import timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
import itertools
from argparse import ArgumentParser
import nexrad_quickplot as nq


def main():
    p = ArgumentParser()
    p.add_argument('start', help='time to start downloading data')
    p.add_argument('stop', help='time to stop downloading data')
    p.add_argument('outdir', help='directory to write data', nargs='?', default='.')
    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('-t', '--timestep', help='time step to download (minutes)', type=int,
                   default=5)
    P = p.parse_args()

    outdir = Path(P.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    start, stop = parse(P.start), parse(P.stop)
# %% NEXRAD
    tnexrad = nq.datetimerange(start, stop, timedelta(minutes=P.timestep))
    print('downloading', len(tnexrad), 'files to', outdir)

    if P.debug:
        for t in tnexrad:
            nq.download(t, outdir)
    else:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(nq.download,
                         tnexrad, itertools.repeat(outdir),
                         timeout=600)
    print()
    

if __name__ == '__main__':
    main()
