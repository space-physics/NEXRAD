#!/usr/bin/env python
"""parallel file downloading for Python 3"""
import urllib.request
from datetime import datetime, timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
#

def datetimerange(start:datetime, stop:datetime, step:timedelta) -> list:
    return [start + i*step for i in range((stop-start) // step)]

def get_goes(t:datetime, outdir:Path, goes:int, mode:str):
    """download GOES file for this time
    https://www.ncdc.noaa.gov/gibbs/image/GOE-13/IR/2017-08-21-06
    """

    dgoes = f'{t.year}-{t.month:02d}-{t.day:02d}-{t.hour:02d}'

    fn = outdir / f"goes{goes:d}-{mode}-{dgoes}.jpg"

    if fn.is_file(): # no clobber
        return

    url = (f'https://www.ncdc.noaa.gov/gibbs/image/GOE-{goes}/{mode}/' + dgoes)

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)


def get_nexrad(t:datetime, outdir:Path):
    """download NEXRAD file for this time
    https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
    """
    fn = outdir/f"nexrad{t.isoformat()}.png"

    if fn.is_file(): # no clobber
        return

    url = ('https://mesonet.agron.iastate.edu/archive/data/' +
           f'{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png')

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start',help='time to start downloading data')
    p.add_argument('stop',help='time to stop downloading data')
    p.add_argument('outdir',help='directory to write data')
    p.add_argument('-goes',help='GOES type (IR, VS, WV)')
    p = p.parse_args()

    outdir = Path(p.outdir).expanduser()
    outdir.mkdir(parents=True,exist_ok=True)

    start, stop = parse(p.start), parse(p.stop)
# %% NEXRAD
    tnexrad = datetimerange(start, stop, timedelta(minutes=5))

    if not p.goes:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
            future_file = {exe.submit(get_nexrad, t, outdir): t for t in tnexrad}
            for f in concurrent.futures.as_completed(future_file):
                t = future_file[f]
# %% GOES13
    tgoes = datetimerange(start, stop, timedelta(hours=3))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        future_file = {exe.submit(get_goes, t, outdir, 13, p.goes): t for t in tgoes}
        for f in concurrent.futures.as_completed(future_file):
            t = future_file[f]