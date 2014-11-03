#!/usr/bin/env python

from distutils.core import setup

setup(name='dotacrunch',
      version='ALPHA 0.1',
      description='Dota Replay Analyzer',
      author='Stefan Hanreich',
      author_email='stefanhani@gmail.com',
      url='https://github.com/lawli3t/dotacrunch',
      packages=["dotacrunch"],
      package_dir = {'': 'src'},
      package_data={'': ['assets/dota2map.png']}
)