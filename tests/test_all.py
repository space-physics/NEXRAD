#!/usr/bin/env python
import pytest
from datetime import datetime
import tempfile
from numpy.testing import run_module_suite
#
import nexrad_quickplot as nq

odir = tempfile.gettempdir()

@pytest.fixture
def test_download_nexrad():
    fn = nq.download(datetime(2018,1,1,0), odir)


if __name__ == '__main__':
   run_module_suite()
