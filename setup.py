#!/usr/bin/env python
"""This is a one-line description of the module.

Author: Matthew Lefavor
Email:  matthew.lefavor@nasa.gov
Date:   2013-04-04

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import distutils.core
import distutils.version



if __name__ == '__main__':
    distutils.core.setup(
        name="reprutils",
        version='1.0',
        description='Helpers for creating __repr__ methods',
        # TODO: long_description='',
        author='Matthew Lefavor',
        author_email='mclefavor@gmail.com',
        # TODO: url=,
        # TODO: download_url=,
        py_modules=['reprutils'],
        classifiers=[
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
            "License :: OSI Approved :: MIT License",
        ]
    )
