#!/usr/bin/env python
"""
keogram example:
python plot-nexrad.py ~/data/2017-08-21/nexrad/ -keo lat 40 -odir ~/data/myplots

Plot stack example:
./plot-nexrad.py ~/data/2017-08-21/nexrad/ -odir ~/data/2017-08-21/nexrad/plots -pat nexrad2017-08-21T14*.png

Panel subplot example:
./plot-nexrad.py ~/data/2017-08-21/nexrad/nexrad2017-08-21T12:00:00.png ~/data/2017-08-21/nexrad/nexrad2017-08-21T12:30:00.png -odir ~/data/2017-08-21/nexrad/plots
"""
from typing import Tuple, List, Optional
import nexrad_quickplot as nq
from pathlib import Path
from argparse import ArgumentParser
try:
    import nexrad_quickplot.plots as nqp
    from matplotlib.pyplot import show, pause
except ImportError:
    nqp = show = pause = None
import seaborn as sns
sns.set_context('paper', font_scale=1.2)

SCALEFN = Path(__file__).parent / 'doc' / 'n0q_ramp.png'


def genplots(P, scalefn: Path):

    odir = Path(P.odir).expanduser() if P.odir else None
# %% file list--panel
    if len(P.datadir) > 1:
        flist = [Path(f).expanduser() for f in P.datadir]
        ofn = odir / f'panel-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
        if not P.quiet and nqp is not None:
            nqp.nexrad_panel(flist, P.wld, ofn, P.lattick, scalefn=scalefn)
        return
# %% glob input directory
    datadir = Path(P.datadir[0]).expanduser()
    flist = [datadir] if datadir.is_file() else sorted(datadir.glob(P.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'did not find files in {datadir} with pattern {P.pat}')
# %% Process / Plot
    if isinstance(P.keo, list) and len(P.keo) == 2:
        ofn = nexrad_keogram(flist, P.keo, P.wld, odir, scalefn=scalefn, quiet=P.quiet)
        print('keogram created at', ofn)
    else:
        nexrad_loop(flist, P.wld, odir, P.lattick, scalefn=scalefn, quiet=P.quiet)
        if odir:
            print('\nImageMagick can convert the PNGs to animated GIF by a command like:')
            print('\nconvert map2018-0101T09*.png out.gif')


def nexrad_keogram(flist: List[Path], keo: List[str],
                   wld: Path, odir: Path=None, scalefn: Path=None, quiet: bool=False) -> Optional[Path]:

    keoreq: Tuple[str, float] = (keo[0], float(keo[1]))

    ofn = odir / f'keo-{keo[0]}{keo[1]}-{flist[0].stem}-{flist[-1].stem}.png' if odir else None
    dkeo = nq.keogram(flist, keoreq, wld)

    if not quiet and nqp is not None:
        nqp.keogram(dkeo, ofn, scalefn=scalefn)

    return ofn


def nexrad_loop(flist: List[Path],
                wld: Path, odir: Optional[Path],
                lattick: float=None, scalefn: Path=None, quiet: bool=False):

    mlp: dict = {}
    for f in flist:
        ofn = odir / ('map' + f.name[6:]) if odir else None
        img = nq.load(f, wld)
        if not quiet and nqp is not None:
            mlp = nqp.overlay2d(img, ofn, mlp, lattick=lattick, scalefn=scalefn)
            if not ofn:  # display only
                pause(1)


def main():
    p = ArgumentParser()
    p.add_argument('datadir', help='directory of NEXRAD PNG data to read', nargs='+')
    p.add_argument('-pat', help='file glob pattern', nargs='?', default='*.png')
    p.add_argument('-wld', help='.wld filename', default=Path(__file__).parent / 'n0q.wld')
    p.add_argument('-keo', help='make keogram at lat/lon value',
                   metavar=('lat/lon', 'value'), nargs=2)
    p.add_argument('-lattick', help='specify specific latitude to have additional tick at',
                   type=float)
    p.add_argument('-odir', help='save graphs to this directory')
    p.add_argument('-q', '--quiet', help='no plots', action='store_true')
    p.add_argument
    P = p.parse_args()

    genplots(P, SCALEFN)

    if show is not None:
        show()


if __name__ == '__main__':
    main()
