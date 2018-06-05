#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = ['python-dateutil', 'numpy', 'imageio', 'scikit-image', 'xarray']
tests_require = ['pytest', 'nose', 'coveralls', 'flake8', 'mypy']

setup(name='NEXRAD_quickplot',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.6.1r',
      url='https://github.com/scivision/nexrad-quick-plot',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      description='easily download and plot NEXRAD weather radar reflectivity data',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests': tests_require,
                      'plots': ['cartopy', 'matplotlib', 'seaborn'], },
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
      script=['download-nexrad.py', 'plot-nexrad.py'],
      include_package_data=True,
      )
