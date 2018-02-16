#!/usr/bin/env python
install_requires = ['numpy','imageio','scikit-image']
tests_require = ['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='NEXRAD_quickplot',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/nexrad-quickplot',
      long_description=open('README.rst').read(),
      description='easily download and plot NEXRAD weather radar reflectivity data',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require},
      python_requires='>=3.6',
	  )

