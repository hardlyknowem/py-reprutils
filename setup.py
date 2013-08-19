#!/usr/bin/env python
"""Setup script for `reprutils` module.

Author: Matthew Lefavor
Email:  matthew.lefavor@nasa.gov
Date:   2013-04-04

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import codecs
import os
from distutils.core import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc = ascii: enc if name == 'mbcs' else None
    codecs.register(func)

DEFAULT_DESCRIPTION = 'Helper Functions for `__repr__` Methods'
if os.path.exists('README.rst'):
    with open('README.rst') as fp:
        LONG_DESCRIPTION = fp.read()
else:
    LONG_DESCRIPTION = DEFAULT_DESCRIPTION

if __name__ == '__main__':
    setup(
        name="reprutils",
        version='1.0',
        description=DEFAULT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author='Matthew Lefavor',
        author_email='mclefavor@gmail.com',
        url='https://github.com/mlefavor/py-reprutils',
        download_url='https://pypi.python.org/pypi/reprutils',
        py_modules=['reprutils'],
        keywords="reprutils, repr, __repr__",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.0",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: MIT License",
        ]
    )
