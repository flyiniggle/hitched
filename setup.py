#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Hitched',
      version='0.1',
      description='Wedding information for Bri and Dan - we\'re getting hitched!',
      author='Dan Thompson',
      author_email='d.thompso@yahoo.com',
      packages=find_packages(),
      install_requires=['CherryPy==10.0.0', 'cheroot==5.0.1', 'jaraco.compat==1.', 'jaraco.timing==1.', 'portend==1.7', 'pypiwin32==219', 'pytz==2016.10', 'six==1.10.0', 'tempora==1.6.1']
     )