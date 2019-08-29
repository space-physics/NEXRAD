#!/usr/bin/env python
import subprocess
import tempfile
from pathlib import Path
import pytest


def test_download_load():
    pytest.importorskip("cartopy")

    with tempfile.TemporaryDirectory() as d:
        odir = Path(d)
        subprocess.check_call(
            ["download_nexrad", "2018-01-01T00:00", "2018-01-01-T00:10", str(odir)]
        )

        flist = sorted(map(str, odir.glob("nexrad*.png")))
        assert len(flist) == 2

        subprocess.check_call(["plot_nexrad", "-q", *flist])


if __name__ == "__main__":
    pytest.main(["-xrsv", __file__])
