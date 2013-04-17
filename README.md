reprutils
=========

This is a simple Python module for reducing the boilerplate code
involved in writing ``__repr__`` methods. This code works for all
Python versions from 2.6 to 3.3.

This software was written by Matthew Lefavor (mclefavor _at_ gmail.com).
The license for this software can be found in the LICENSE text file
accompanying this distribution.

Installation
------------

Download the reprutils source archive from PyPI. After downloading,
unpack the archive and run the standard "python setup.py install" with
your favorite Python interpreter:

    my-shell$ tar -xf reprutils-1.0.tar.gz
    my-shell$ cd reprutils-1.0
    my-shell$ python setup.py install

You may need to use ``sudo`` for the last step, depending on the
location of your python interpreter. This package is also installable
via ``pip``, and Windows users can use a graphical installer found on
the PyPI page.

Overview and Examples
---------------------

In Python, an object's ``__repr__`` method is supposed to return a
string giving a standard representation of the object. By convention,
the strings returned by a ``__repr__`` method should be (whenever
possible) a valid Python expression that could return an equivalent
object. This means returning a string that looks like a call to the
object's constructor (fully qualified with the module name). But the
code to do so is typically repetitive and hard to read, particularly
if you wish to want to dynamically access the object's module and class
name. This module provides functions and descriptors for creating some
common ``__repr__`` patterns to save time, improve code readability, and
promote the good coding practice of creating ``__repr__`` methods for
objects (don't debug without one!).

The ``standard_repr`` function is a general-purpose function for
creating a constructor-formatted repr as described above. The user can
pass any arbitrary values to appear as arguments or keyword arguments to
the constructor. That said, most use cases don't require arbitrary
values; the values to appear in the resulting string are attributes of
the object. This case is simplified by the `GetattrRepr` descriptor.
Example usages of both are given below; for more information about
nitty-gritty details (like the ordering of keyword arguments) and some
syntactic sugar, consult the docstrings for ``standard_repr`` and
``GetattrRepr``.

    >>> from reprutils import standard_repr, GetattrRepr
    >>> class DataPoint(object):
    ...     """Represents a single point of data."""
    ...     def __init__(self, time, value, units=None):
    ...         """Initialize the DataPoint.
    ...
    ...         @param time: Time (in seconds) of the observation
    ...         @param value: Recorded value at the time of the observation.
    ...         @param units: Units of the measurement
    ...
    ...         """
    ...         self.time = time
    ...         self.value = value
    ...         self.units = units
    ...
    ...     __repr__ = GetattrRepr('time', 'value', units='units')
    ...
    >>> dp = DataPoint(1200, 5.3, units="Newtons")
    >>> dp
    "__main__.DataPoint(1200, 5.3, units='Newtons')"
    >>> class DataPoint2(object):
    ...     """Represents a single point of data."""
    ...     def __init__(self, time, value, units=None):
    ...         """Initialize the DataPoint.
    ...
    ...         @param time: Time (in seconds) of the observation
    ...         @param value: Recorded value at the time of the observation.
    ...         @param units: Units of the measurement
    ...
    ...         """
    ...         self.time = time + 1800   # Correct timezone
    ...         self.value = value - 2.5  # Correct for widget offset
    ...         self.units = units
    ...
    ...     def __repr__(self):
    ...         """Return a standard representation of the object."""
    ...         return standard_repr(self, [self.time - 7000, value + 2.5],
    ...                              [('units', self.units)])
    ...
    >>> dp = DataPoint2(24000, 2.6, units="Newtons")
    >>> dp
    "__main__.DataPoint2(24000, 2.6, units='Newtons')"
