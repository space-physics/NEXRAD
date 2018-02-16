#!/usr/bin/env python
from pathlib import Path
import imageio
import skimage.transform
from matplotlib.pyplot import figure,show
#from matplotlib.colors import rgb_to_hsv
import cartopy
#
from nexrad_quickplot import wld2mesh
#from metpy.plots import ctables

#def extract_colormap():
#    norm, cmap = ctables.registry.get_with_steps('NWSReflectivity', -75, 0.5)
#    rgb = cmap(np.arange(16))

#    return rgb

# WGS84 is the default, just calling it out explicity so somene doesn't wonder.
GREF = cartopy.crs.PlateCarree()#globe=cartopy.crs.Globe(ellipse='WGS84')

def loadimg(fn:Path):
    """loads and modifies image for plotting"""

    img = imageio.imread(str(fn))
    img = skimage.transform.resize(img, (img.shape[0]//8, img.shape[1]//8),
                                   mode='constant',cval=255,
                                    preserve_range=True).astype(img.dtype)
    # make transparent (arbitrary)
    img[...,-1] = 128

    mask = img[...,:3].all(axis=2) == 0
    img[mask,:3] = 255  # make no signal be white

    return img


def plotnexrad(img, fn:Path, lat:list, lon:list):
    """plot NEXRAD reflectivity on map coordinates"""
    #hsv = rgb_to_hsv(d)

    ax = figure(figsize=(15,10)).gca(projection=GREF)

    ax.set_title(fn.name)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                  '50m',
                                  linestyle=':',linewidth=0.5, edgecolor='grey', facecolor='none'))

    labels = [[-117.1625, 32.715, 'San Diego'],
              [-87.9073, 41.9742, 'KORD' ],
              [-90.3755, 38.7503,'KSUS'],
              [-97.040443,32.897480,'KDFW'],
              [-104.6731667,39.8616667,'KDEN'],
              [ -111.1502604,45.7772358,'KBZN'],
              [ -106.6082622,35.0389316,'KABQ']
              ]
    if 0:
      for l in labels:
        ax.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
        ax.annotate(l[2], xy = (l[0], l[1]), xytext = (3, 3), textcoords = 'offset points')

    ax.imshow(img,origin='upper',
          extent=[lon[0],lon[-1],lat[0],lat[-1]],
          transform=GREF)



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of NEXRAD PNG data to read')
    p.add_argument('pat',help='file glob pattern',nargs='?', default='*.png')
    p.add_argument('-N',help='number of images to process',type=int,default=1)
    p.add_argument('-wld',help='.wld filename',default='n0q.wld')
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()
    if datadir.is_file():
        flist = [datadir]
    else:
        flist = list(datadir.glob(p.pat))

    img = imageio.imread(str(flist[0]))
    lat, lon = wld2mesh(p.wld, img.shape[:2])


    for f in flist:
        img = loadimg(f)
        plotnexrad(img, f, lat, lon)
        show()
        break
