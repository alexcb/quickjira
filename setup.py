#!/usr/bin/env python3

from setuptools import setup

setup(name='quickjira',
  version='0.1',
  description='local dns resolver',
  author='Alex Couture-Beil',
  url='https://github.com/alexcb/quickjira',
  packages=[
      'quickjira',
      ],
  install_requires=[
    'requests',
    ],
 )
