#!/usr/bin/env python
"""This is a one-line description of the module.

Author: Matthew Lefavor
Email:  matthew.lefavor@nasa.gov
Date:   2013-04-04

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from distutils.core import setup

if __name__ == '__main__':
    setup(
        name="reprutils",
        version='1.0',
        description='Standard __repr__ Utilities',
        long_description="""\
Helper functions for common `__repr__` patterns
-----------------------------------------------

Descriptors and functions for use in creating `__repr__` methods for
Python objects according to common patterns. Currently, support is
implemented for creating constructor-style reprs (results which look
like a valid python constructor to create a new equivalent object).

""",
        author='Matthew Lefavor',
        author_email='mclefavor@gmail.com',
        url='https://github.com/mlefavor/py-reprutils',
        # TODO: download_url=,
        py_modules=['reprutils'],
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
