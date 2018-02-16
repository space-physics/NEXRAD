#!/usr/bin/env python
import unittest
from datetime import datetime
import tempfile
#
import nexrad_quickplot as nq

class BasicTests(unittest.TestCase):

    def test_download_nexrad(self):
        nq.get_nexrad(datetime(2018,1,1,0), tempfile.gettempdir())

if __name__ == '__main__':
    unittest.main()
