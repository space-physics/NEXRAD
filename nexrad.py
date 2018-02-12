#!/usr/bin/env python
import urllib.request
from datetime import datetime, timedelta
from dateutil.parser import parse
from pathlib import Path
#
base = 'https://mesonet.agron.iastate.edu/archive/data/'
DT = timedelta(minutes=5)  # time resolution of NEXRAD composite data since 1995


def datetimerange(start:datetime, stop:datetime, step:timedelta) -> list:
    return [start + i*step for i in range((stop-start) // step)]


def get_composite(start:datetime, stop: datetime, outdir:Path):
    tlist = datetimerange(start,stop,DT)

    print('downloading',len(tlist),'files to',outdir)
    for t in tlist:
        url = base + f'{t.year}/{t.month:02d}/{t.day:02d}/GIS/uscomp/n0q_{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}.png'
        fn = outdir/f"nexrad{t.isoformat()}.png"
        print(fn,end='\r')
        urllib.request.urlretrieve(url, fn)


#https://mesonet.agron.iastate.edu/archive/data/2018/02/12/GIS/uscomp/n0q_201802120000.png
#https://mesonet.agron.iastate.edu/archive/data/2017/08/19/GIS/uscomp/n0q_2017081900.png

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start',help='time to start downloading data')
    p.add_argument('stop',help='time to stop downloading data')
    p.add_argument('-o','--outdir',help='directory to write data',default='~/data/')
    p = p.parse_args()

    outdir = Path(p.outdir).expanduser()
    outdir.mkdir(parents=True,exist_ok=True)

    get_composite(parse(p.start), parse(p.stop), outdir)
