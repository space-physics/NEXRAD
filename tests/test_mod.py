#!/usr/bin/env python
import pytest
from pytest import approx
from pathlib import Path
from datetime import datetime
import os
#
import nexrad_quickplot as nq

odir = Path(__file__).parent


@pytest.fixture
def download_nexrad() -> Path:
    fn = nq.download(datetime(2018, 1, 1, 0), odir)

    if os.name == 'nt':
        assert fn.name == 'nexrad2018-01-01T00-00-00.png'
    else:
        assert fn.name == 'nexrad2018-01-01T00:00:00.png'

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
