#!/usr/bin/env python
"""parallel file downloading for Python 3"""
import urllib.request
from datetime import datetime, timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
#
#https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
BASE = 'https://mesonet.agron.iastate.edu/archive/data/'
DT = timedelta(minutes=5)  # time resolution of NEXRAD composite data since 1995


def datetimerange(start:datetime, stop:datetime, step:timedelta) -> list:
    return [start + i*step for i in range((stop-start) // step)]


def get_file(t:datetime, outdir:Path):
    """download NEXRAD file for this time"""
    fn = outdir/f"nexrad{t.isoformat()}.png"

    if fn.is_file(): # no clobber
        return

    url = BASE + f'{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png'

    print(fn,end='\r')
    urllib.request.urlretrieve(url, fn)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start',help='time to start downloading data')
    p.add_argument('stop',help='time to stop downloading data')
    p.add_argument('-o','--outdir',help='directory to write data',default='~/data/')
    p = p.parse_args()

    outdir = Path(p.outdir).expanduser()
    outdir.mkdir(parents=True,exist_ok=True)

    tlist = datetimerange(parse(p.start), parse(p.stop), DT)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        future_file = {exe.submit(get_file, t, outdir): t for t in tlist}
        for f in concurrent.futures.as_completed(future_file):
            t = future_file[f]