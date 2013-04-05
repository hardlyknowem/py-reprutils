#!/usr/bin/env python
"""This is a one-line description of the module.

Author: Matthew Lefavor
Email:  matthew.lefavor@nasa.gov
Date:   2013-04-03

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest

PY2 = sys.version_info() < (3,)

from lib699.enhancements.reprutils import standard_repr, GetattrRepr


class DummyClass(object):
    """A dummy class for testing reprs."""
    pass


class TestStandardRepr(unittest.TestCase):
    """Test the standard_repr method."""
    def setUp(self):
        """Create an instance of the dummy class."""
        self.dc = DummyClass()

    def _helper(self, target, *args, **kwargs):
        """Assert that calling standard_repr on self.dc returns target.

        Also asserts the result is the unicode type, not bytes.

        """
        result = standard_repr(self.dc, *args, **kwargs)
        self.assertIsInstance(result, six.text_type)
        self.assertEqual(result, target)

    def test_positional(self):
        """Test standard_repr with positional arguments."""
        self._helper('test_reprutils.DummyClass()')
        self._helper('test_reprutils.DummyClass(1)', 1)
        self._helper('test_reprutils.DummyClass(1, 2, 3)', 1, 2, 3)

    def test_kwargs(self):
        """Test standard_repr with keyword arguments."""
        self._helper('test_reprutils.DummyClass(arg=1)', arg=1)
        self._helper('test_reprutils.DummyClass(arg1=1, arg2=2, arg3=3)',
                     arg1=1, arg2=2, arg3=3)
        self._helper('test_reprutils.DummyClass(0, -1, arg=1)', 0, -1, arg=1)
        self._helper('test_reprutils.DummyClass(0, 9, arg1=1, arg2=2, arg3=3)',
                     0, 9, arg1=1, arg2=2, arg3=3)

    def test_repr(self):
        """Assert the repr is being called on arguments."""
        self._helper('test_reprutils.DummyClass(True)', True)
        self._helper('test_reprutils.DummyClass(None)', None)
        if PY2:
            self._helper("test_reprutils.DummyClass(u'None')", 'None')
            self._helper("test_reprutils.DummyClass('None')", b'None')
        else:
            self._helper("test_reprutils.DummyClass('None')", 'None')
            self._helper("test_reprutils.DummyClass(b'None')", b'None')

    def tearDown(self):
        """Remove the old dummy object."""
        del self.dc

class TestGetattrRepr(unittest.TestCase):
    """

    """
    def setUp(self):
        """Create an instance of the dummy class."""
        self.dc = DummyClass()
        self.dc.a = 1
        self.dc.b = 2
        self.dc.c = 3
        self.dc.x = None
        self.dc.y = True
        self.dc.z = 'asdf'

    def tearDown(self):
        del DummyClass.__repr__
        del self.dc

    def test_positional(self):
        """Test standard_repr with positional arguments."""
        DummyClass.__repr__ = GetattrRepr()
        self.assertEqual(repr(self.dc), 'test_reprutils.DummyClass()')

        DummyClass.__repr__ = GetattrRepr('a')
        self.assertEqual(repr(self.dc), 'test_reprutils.DummyClass(1)')

        DummyClass.__repr__ = GetattrRepr('a', 'b', 'c')
        self.assertEqual(repr(self.dc), 'test_reprutils.DummyClass(1, 2, 3)')

    def test_kwargs(self):
        """Test standard_repr with keyword arguments."""
        DummyClass.__repr__ = GetattrRepr(arg='a')
        self.assertEqual(repr(self.dc), 'test_reprutils.DummyClass(arg=1)')

        DummyClass.__repr__ = GetattrRepr(arg1='a', arg2='b', arg3='c')
        self.assertEqual(repr(self.dc),
                         'test_reprutils.DummyClass(arg1=1, arg2=2, arg3=3)')

        DummyClass.__repr__ = GetattrRepr('x', 'y', arg='a',)
        self.assertEqual(repr(self.dc),
                         'test_reprutils.DummyClass(None, True, arg=1)')

        DummyClass.__repr__ = GetattrRepr('x', 'y', arg1='a', arg2='b',
                                          arg3='c')
        self.assertEqual(repr(self.dc),
                         'test_reprutils.DummyClass(None, True, arg1=1, '
                         'arg2=2, arg3=3)')

    def test_sugar(self):
        """Test the sugared list syntax for keyword arguments."""
        DummyClass.__repr__ = GetattrRepr(['a', 'b', 'c'])
        self.assertEqual(repr(self.dc),
                         'test_reprutils.DummyClass(a=1, b=2, c=3)')
