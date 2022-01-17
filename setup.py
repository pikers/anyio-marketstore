#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name='anyio-marketstore',
    version='0.1a0',
    packages=['anyio_marketstore'],
    package_dir={'':'src'},
    install_requires=[
        'numpy',
        'pandas',
        'purerpc'
    ]
)
