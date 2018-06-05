#!/usr/bin/env python
import pytest
from pathlib import Path
import xarray
from datetime import datetime
#
import nexrad_quickplot as nq

odir = Path(__file__).parent
WLD = odir.parent / 'n0q.wld'


@pytest.fixture
def test_download_nexrad() -> Path:
    fn = nq.download(datetime(2018, 1, 1, 0), odir)
    return fn


def test_load():
    fn: Path = test_download_nexrad()
    img: xarray.DataArray = nq.load(fn, WLD)

    assert img.ndim == 3  # RGB image


def test_keo():
    ilat = 45.
    fn: Path = test_download_nexrad()
    keo: xarray.DataArray = nq.keogram([fn], ['lat', ilat], WLD)

    assert keo.ndim == 3

    keo.lat == pytest.approx(ilat)


if __name__ == '__main__':
    pytest.main()
