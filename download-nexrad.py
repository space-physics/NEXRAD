#!/usr/bin/env python
"""parallel file downloading for Python 3"""
from datetime import timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
import itertools
#
import nexrad_quickplot as nq

dtmin = 5

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start', help='time to start downloading data')
    p.add_argument('stop', help='time to stop downloading data')
    p.add_argument('outdir', help='directory to write data')
    P = p.parse_args()

    outdir = Path(P.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    start, stop = parse(P.start), parse(P.stop)
# %% NEXRAD
    tnexrad = nq.datetimerange(start, stop, timedelta(minutes=dtmin))
    print('downloading', len(tnexrad), 'files to', outdir)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(nq.download,
                     tnexrad, itertools.repeat(outdir),
                     timeout=600)
    print()
