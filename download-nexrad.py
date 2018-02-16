#!/usr/bin/env python
"""parallel file downloading for Python 3"""
from datetime import timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
#
from nexrad_quickplot import get_nexrad, datetimerange

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start',help='time to start downloading data')
    p.add_argument('stop',help='time to stop downloading data')
    p.add_argument('outdir',help='directory to write data')
    p = p.parse_args()

    outdir = Path(p.outdir).expanduser()
    outdir.mkdir(parents=True,exist_ok=True)

    start, stop = parse(p.start), parse(p.stop)
# %% NEXRAD
    tnexrad = datetimerange(start, stop, timedelta(minutes=5))
    print('downloading',len(tnexrad),'files to',outdir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        future_file = {exe.submit(get_nexrad, t, outdir): t for t in tnexrad}
        for f in concurrent.futures.as_completed(future_file):
            t = future_file[f]
