#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Hitched',
      version='0.1',
      description='Wedding information for Bri and Dan - we\'re getting hitched!',
      author='Dan Thompson',
      author_email='d.thompso@yahoo.com',
      packages=find_packages(),
      install_requires=["cherrypy"]
     )