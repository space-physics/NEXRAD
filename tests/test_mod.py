#!/usr/bin/env python
import pytest
from pytest import approx
from pathlib import Path
from datetime import datetime, date
#
import nexrad_quickplot as nq

odir = Path(__file__).parent


@pytest.fixture
def download_nexrad() -> Path:
    fn = nq.download(datetime(2018, 1, 1, 0), odir)

    fn = nq.download(date(2018, 1, 1), odir)  # verifying date and noclobber OK

    return fn


def test_load():
    fn = download_nexrad()
    img = nq.load(fn)

    assert img.ndim == 3  # RGB image


def test_keo():
    ilat = 45.
    fn = download_nexrad()
    keo = nq.loadkeogram([fn], ['lat', ilat])

    assert keo.ndim == 3

    keo.lat == approx(ilat)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
