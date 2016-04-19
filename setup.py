#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from setuptools import find_packages
from setuptools import setup
import stgadm.globalvar

version = stgadm.globalvar.version

setup(
    name="STGAdm",
    version=version,
    description="Storage Disk Administration Tool (EMC VNX, VMAX and "
                "IBM DS8K)",
    long_description=open('README.rst').read(),
    author="Kairo Araujo",
    author_email="kairo@kairo.eti.br",
    maintainer="Kairo Araujo",
    maintainer_email="kairo@kairo.eti.br",
    url="https://github.com/kairoaraujo/STGAdm/",
    keywords="Storage Disk Administration Tool (EMC VNX, VMAX and IBM DS8K)",
    packages=find_packages(exclude=['*.test', 'tests.*']),
    package_data={'': ['License.txt']},
    include_package_data=True,
    license='BSD',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving',
        'Topic :: System :: Hardware',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.8',
    ],
)
