#!/usr/bin/env python
install_requires = ['python-dateutil','numpy','imageio>=2.3','scikit-image','xarray']
tests_require = ['pytest','nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='NEXRAD_quickplot',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.5.0',
      url='https://github.com/scivision/nexrad-quickplot',
      long_description=open('README.rst').read(),
      description='easily download and plot NEXRAD weather radar reflectivity data',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plots':['cartopy','matplotlib'],},
      python_requires='>=3.6',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      script=['download-nexrad.py','plot-nexrad.py'],
      include_package_data=True,
	  )

