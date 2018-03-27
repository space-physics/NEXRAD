.. image:: https://travis-ci.org/scivision/nexrad-quick-plot.svg?branch=master
    :target: https://travis-ci.org/scivision/nexrad-quick-plot

.. image:: https://coveralls.io/repos/github/scivision/nexrad-quick-plot/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/nexrad-quick-plot?branch=master


===================
Nexrad Quick-plot
===================
Easy Python download and plot NEXRAD compositive reflectivity.
GOES weather satellite moved to its `own repo <https://github.com/scivision/goes-quickplot>`_.

Install
=======
::

    python -m pip install -e .

Usage
=====


1. Get `NEXRAD reflectivity data <https://mesonet.agron.iastate.edu/docs/nexrad_composites/>`_ with parallel download::

        python download-nexrad.py start stop outdir

   example: download from 2018-01-01 to 2018-01-02 to ``~/data/nexrad``::

        python download-nexrad.py 2018-01-01T00 2018-01-03T00 ~/data/nexrad

2. Plot NEXRAD reflectivity data georegistered via Cartopy::

        python plot-nexrad.py ~/data/nexrad/

   Plot a specific file::

        python plot-nexrad.py ~/data/nexrad/2018-01-01T12:35:00.png




Coordinates
===========

EPSG:4326 coordinates (WGS84) are in .wld files, which are generally the same for wide time spans of data.
The `.wld format <https://mesonet.agron.iastate.edu/docs/radmapserver/howto.html#toc3.3>`_ is like::

    0.005 (size of pixel in x direction)
    0.0 (rotation of row) (Typically zero)
    0.0 (rotation of column) (Typically zero)
    -0.005 (size of pixel in y direction)
    -126.0 (x coordinate of centre of upper left pixel in map units--here it's WGS84 longitude)
    50.0 (y coordinate of centre of upper left pixel in map units--here it's WGS84 latitude)


Notes
=====


Mass image downscaling
----------------------
For initial analysis, the original Nexrad image size of 14440 x 5000 pixels may be too high to complete in a reasonable time.
I choose to downsize by a factor of 10, which takes a long time, but is a one-time process.
This is done using all CPU cores via GNU Parallel and ImageMagick on Linux or Mac.

.. code: bash

    mkdir orig
    cp *.png orig

    find . -maxdepth 1 -name "*.png" | nice parallel mogrify -scale 10%


GNU Parallel is available via:

* Linux: ``apt install parallel``
* Mac: ``brew install parallel``