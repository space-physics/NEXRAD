[![Travis-CI](https://travis-ci.org/scivision/nexrad-quick-plot.svg?branch=master)](https://travis-ci.org/scivision/nexrad-quick-plot)
[![Coveralls.io](https://coveralls.io/repos/github/scivision/nexrad-quick-plot/badge.svg?branch=master)](https://coveralls.io/github/scivision/nexrad-quick-plot?branch=master)
[![AppVeyor Build Station](https://ci.appveyor.com/api/projects/status/jmiiyri2xqdvu5wm?svg=true)](https://ci.appveyor.com/project/scivision/nexrad-quick-plot)
[![image](https://img.shields.io/pypi/pyversions/NEXRAD-quickplot.svg)](https://pypi.python.org/pypi/NEXRAD-quickplot)
[![image](https://img.shields.io/pypi/format/NEXRAD-quickplot.svg)](https://pypi.python.org/pypi/NEXRAD-quickplot)
[![Maintainability](https://api.codeclimate.com/v1/badges/d2df020d3c1e6522412a/maintainability)](https://codeclimate.com/github/scivision/nexrad-quick-plot/maintainability)
[![PyPi Download stats](http://pepy.tech/badge/NEXRAD-quickplot)](http://pepy.tech/project/NEXRAD-quickplot)

# Nexrad Quick-plot

Easy Python download and plot NEXRAD N0Q compositive reflectivity. 
Uses RGB high resolution PNG images of North America.

Tested with `pytest`, `flake8` and `mypy` type checking.

## Install

    python -m pip install -e .

## Usage

RGB data scaling: NEXRAD N0Q base reflectivity maps.

* Black: No Data
* -32 dBZ .. 90 dBZ
* 0.5 dBZ increment

![NEXRAD N0Q RGB scaling](doc/n0q_ramp.png)

### Download NEXRAD data

Get 
[NEXRAD reflectivity data](https://mesonet.agron.iastate.edu/docs/nexrad_composites/) 
with parallel download:

   download-nexrad start stop outdir

example: download from 2018-01-01 to 2018-01-02 to `~/data/nexrad`:

    download-nexrad 2018-01-01T00 2018-01-03T00 ~/data/nexrad

### Plot NEXRAD reflectivity data

(georegistered via Cartopy)

Plot all data in directory:

    plot-nexrad ~/data/nexrad/

Plot a specific file (subplots if multiple files specified):

    plot-nexrad ~/data/nexrad/2018-01-01T12:35:00.png

Plot via file glob match:

    plot-nexrad ~/data/nexrad/ -pat 2018-01-01T12*.png
    
Keogram (specify lat or lon and value):

    plot-nexrad ~/data/2017-08-21/nexrad/ -keo lat 40 

## Coordinates

EPSG:4326 coordinates (WGS84) are in .wld files, which are generally the
same for wide time spans of data. The [.wld
format](https://mesonet.agron.iastate.edu/docs/radmapserver/howto.html#toc3.3)
is like:

    0.005 (size of pixel in x direction)
    0.0 (rotation of row) (Typically zero)
    0.0 (rotation of column) (Typically zero)
    -0.005 (size of pixel in y direction)
    -126.0 (x coordinate of centre of upper left pixel in map units--here it's WGS84 longitude)
    50.0 (y coordinate of centre of upper left pixel in map units--here it's WGS84 latitude)

## Notes


### Mass image downscaling

For initial analysis, the original Nexrad image size of 12200 x 5400
pixels may be too high to complete in a reasonable time. I choose to
downsize by a factor of 10, which takes a long time, but is a one-time
process.

```bash
mkdir orig
cp *.png orig

nice mogrify -scale 10% "*.png"
```

If you have trouble with this being very slow, try:

```bash
MAGICK_TEMPORARY_PATH=/run/shm nice mogrify -scale 10% "*.png"
```


