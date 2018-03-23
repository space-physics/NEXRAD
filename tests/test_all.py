#!/usr/bin/env python
from datetime import datetime
import tempfile
from numpy.testing import run_module_suite
#
import nexrad_quickplot as nq


def test_download_nexrad():
    with tempfile.TemporaryDirectory() as d:
        nq.download(datetime(2018,1,1,0), d)


if __name__ == '__main__':
   run_module_suite()
