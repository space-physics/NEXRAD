[![Build Status](https://travis-ci.org/scivision/NEXRADutils.svg?branch=master)](https://travis-ci.org/scivision/NEXRADutils)
[![Coverage Status](https://coveralls.io/repos/github/scivision/NEXRADutils/badge.svg?branch=master)](https://coveralls.io/github/scivision/NEXRADutils?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/dasnnsarbyankxqb?svg=true)](https://ci.appveyor.com/project/scivision/nexradutils)
[![Maintainability](https://api.codeclimate.com/v1/badges/05529f213d77cfa3c1f2/maintainability)](https://codeclimate.com/github/scivision/NEXRADutils/maintainability)
[![image](https://img.shields.io/pypi/pyversions/NEXRADutils.svg)](https://pypi.python.org/pypi/NEXRADutils)
[![image](https://img.shields.io/pypi/format/NEXRADutils.svg)](https://pypi.python.org/pypi/NEXRADutils)

[![PyPi Download stats](http://pepy.tech/badge/NEXRADutils)](http://pepy.tech/project/NEXRADutils)

# NEXRAD utilities

Easy Python download and plot NEXRAD N0Q compositive reflectivity.
Uses RGB high resolution PNG images of North America.

Tested with `pytest`, `flake8` and `mypy` type checking.

## Install
```sh
python -m pip install -e .
```

## Usage

RGB data scaling: NEXRAD N0Q base reflectivity maps.

* Black: No Data
* -32 dBZ .. 90 dBZ
* 0.5 dBZ increment

![NEXRAD N0Q RGB scaling](doc/n0q_ramp.png)

These data are reduced fidelity RGB images.
We use `xarray.DataArray` and plot image by image.
For high-fidelity science data, the lower level data are needed--contact us if interested.

```python
import nexradutils as nq

dat = nq.load('~/data/2015-01-19/nexrad/nexrad2015-01-19T01:15:00.png')

>>> dat
<xarray.DataArray (lat: 540, lon: 1220, color: 3)>
array([[[255, 255, 255],
        [255, 255, 255],
        ...,
        [255, 255, 255],
        [255, 255, 255]]], dtype=uint8)
Coordinates:
  * lat      (lat) float64 23.0 23.05 23.1 23.15 23.2 23.25 23.3 23.35 23.4 ...
  * lon      (lon) float64 -126.0 -125.9 -125.9 -125.8 -125.8 -125.7 -125.7 ...
  * color    (color)  'R' 'G' 'B'
Attributes:
    filename:  ~/data/nexrad2015-01-19T01:15:00.png
    wldfn:     None
    time:      2015-01-19 01:15:00
```

`.lat` and `.lon` are vectors of geodetic latitude and longitude respectively, computed based on the `.wld` file corresponding to the images.




### Download NEXRAD data

Get
[NEXRAD reflectivity data](https://mesonet.agron.iastate.edu/docs/nexrad_composites/)
with parallel download:
```sh
download-nexrad start stop outdir
```

example:
download from 2018-01-01 to 2018-01-02 to `~/data/nexrad`:
```sh
download-nexrad 2018-01-01T00 2018-01-03T00 ~/data/nexrad
```

### Plot NEXRAD reflectivity data

NEXRAD plots are georegistered via 
[Cartopy](https://pypi.org/project/Cartopy/), 
which is the replacement for 
[deprecated Basemap](https://www.scivision.co/cartopy-replace-deprecated-basemap/)

* Plot all data in directory:
  ```sh
  plot-nexrad ~/data/nexrad/
  ```
* Plot a specific file (subplots if multiple files specified):
  ```sh
  plot-nexrad ~/data/nexrad/2018-01-01T12:35:00.png
  ```
* Plot via file glob match:
  ```sh
  plot-nexrad ~/data/nexrad/ -pat 2018-01-01T12*.png
  ```
* Keogram (specify lat or lon and value):
  ```sh
  plot-nexrad ~/data/2018-01-01/nexrad/ -keo lat 40
  ```

## Notes

### Coordinates

EPSG:4326 coordinates (WGS84) are in `.wld` files, which are generally the
same for wide time spans of data. The
[.wld format](https://mesonet.agron.iastate.edu/docs/radmapserver/howto.html#toc3.3)
is like:
```
0.005 (size of pixel in x direction)
0.0 (rotation of row) (Typically zero)
0.0 (rotation of column) (Typically zero)
-0.005 (size of pixel in y direction)
-126.0 (x coordinate of centre of upper left pixel in map units--here it's WGS84 longitude)
50.0 (y coordinate of centre of upper left pixel in map units--here it's WGS84 latitude)
```


### Mass image downscaling

For initial analysis, the original Nexrad image size of 12200 x 5400 pixels may be too high to complete in a reasonable time.
I choose to downsize by a factor of 10, which takes a long time, but is a one-time process.

```bash
mkdir orig
cp *.png orig

nice mogrify -scale 10% "*.png"
```

If you have trouble with this being very slow, try:

```bash
MAGICK_TEMPORARY_PATH=/run/shm nice mogrify -scale 10% "*.png"
```


