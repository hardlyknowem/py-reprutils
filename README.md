reprutils
=========

This is a simple Python module for reducing the boilerplate code
involved in writing `__repr__` methods.

Installation
------------

Download the reprutils source archive from PyPI. After downloading,
unpack the archive and run the standard "python setup.py install" with
your favorite Python interpreter:

    my-shell$ tar -xf reprutils-1.0.tar.gz
    my-shell$ cd reprutils-1.0
    my-shell$ python setup.py install

That's it. This is also installable via `pip`, and Windows users can find
a graphical installer on the Python page.

Overview and Examples
---------------------

In Python, an object's `__repr__` method is supposed to return a string
giving a standard representation of the object. By convention, the
strings returned by a `__repr__` method should be (whenever possible) a
valid Python expression that could return an equivalent object. This
means returning a string that looks like a call to the object's
constructor (fully qualified with the module name). But the code to do
so is often unreadable, and in order to dynamically access the object's
module (to defend against inaccuracies after moving the class to another
module) is not particularly readable. This module provides functions and
descriptors for creating some common `__repr__` patterns.

The `standard_repr` function is a general-purpose function for creating
a constructor-formatted repr. The user can pass any arbitrary values
to appear as arguments or keyword arguments to the constructor. That
said, most use cases don't require arbitrary values; the values to
appear in the `__repr__` string are simply attributes of the object. For
this case the user can use the `GetattrRepr` descriptor. Example usages
of both are given below; for more information about the handling of
keyword arguments and their ordering, consult the docstrings for
`standard_repr` and `GetattrRepr`.

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
