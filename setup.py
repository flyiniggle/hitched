#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Hitched',
      version='0.1',
      description='Wedding information for Bri and Dan - we\'re getting hitched!',
      author='Dan Thompson',
      author_email='d.thompso@yahoo.com',
      packages=find_packages(),
      install_requires=['CherryPy==10.0.0', 'cheroot==5.0.1', 'pymongo==3.4.0', 'jaraco.compat==1.2', 'jaraco.timing==1.3.1', 'portend==1.7', 'pytz==2016.10', 'six==1.10.0', 'tempora==1.6.1']
     )