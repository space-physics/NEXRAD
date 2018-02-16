===================
Nexrad-quick-plot
===================
Easy Python download and plot NEXRAD compositive reflectivity  and GOES PNGs by date/time

Install
=======
::

    python -m pip install -e .

Usage
=====
Currently, this program is for NEXRAD and GOES.

NEXRAD
------

1. Get `NEXRAD reflectivity data <https://mesonet.agron.iastate.edu/docs/nexrad_composites/>`_ with parallel download::

        python download-nexrad.py start stop outdir

   example: download from 2018-01-01 to 2018-01-02 to ``~/data/nexrad``::

        python download-nexrad.py 2018-01-01T00 2018-01-03T00 ~/data/nexrad

2. Plot NEXRAD reflectivity data georegistered via Cartopy::

        python plot-nexrad.py ~/data/nexrad/

   Plot a specific file::

        python plot-nexrad.py ~/data/nexrad/2018-01-01T12:35:00.png


GOES
----

1. Get `GOES data <hhttps://www.ncdc.noaa.gov/gibbs//>`_ with parallel download::

        python download-goes.py goesnum start stop outdir

   example: download IR from GOES-13 2018-01-01 to 2018-01-02 to ``~/data/goes13``::

        python download-goes.py 13 IR 2018-01-01T00 2018-01-03T00 ~/data/goes13

2. Plot GOES IR data georegistered via Cartopy::

        python plot-goes.py ~/data/goes13

   Plot a specific file::

        python plot-goes.py ~/data/nexrad/2018-01-01T12:35:00.png



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
