===================
Nexrad-quick-plot
===================
Quick Python script to download and plot NEXRAD compositive reflectivity PNGs by date/time


Usage
=====

1. Gets `NEXRAD data <http://mesonet.agron.iastate.edu/docs/nexrad_composites/>`_ with clean Python3 multithreading::
   
        python download-nexrad.py start stop outdir
   
   for example, to download from 2018-02-01 to 2018-02-05 to ``~/data/nexrad``::
   
        python download-nexrad.py 2018-02-01T00 2018-02-06T00 ~/data/nexrad

2. Plot data georegistered via Cartopy::

        python plot-nexrad.py ~/data/nexrad/
        
        
Coordinates
===========

EPSG:4326 coordinates (WGS84) are in .wld files, which are generally the same for wide time spans of data.
The ```.wld`` format <https://mesonet.agron.iastate.edu/docs/radmapserver/howto.html#toc3.3>`_ is::

    0.005 (size of pixel in x direction)
    0.0 (rotation of row) (Typically zero)
    0.0 (rotation of column) (Typically zero)
    -0.005 (size of pixel in y direction)
    -126.0 (x coordinate of centre of upper left pixel in map units--here it's WGS84 longitude)
    50.0 (y coordinate of centre of upper left pixel in map units--here it's WGS84 latitude) 
