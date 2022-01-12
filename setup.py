#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name='trio-marketstore',
    version='0.1a0',
    packages=['trio_marketstore'],
    package_dir={'':'src'},
    install_requires=[
        'purerpc'
    ]
)
