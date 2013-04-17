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

PY2 = sys.version_info < (3,)

from reprutils import standard_repr, GetattrRepr


class DummyClass(object):
    """A dummy class for testing reprs."""
    pass


class TestStandardRepr(unittest.TestCase):
    """Test the standard_repr method."""
    def setUp(self):
        """Create an instance of the dummy class."""
        self.dc = DummyClass()

    def _helper(self, target, args=None, kwargs=None):
        """Assert that calling standard_repr on self.dc returns target.

        Also asserts the result is the unicode type, not bytes.

        """
        result = standard_repr(self.dc, args, kwargs)
        self.assertIsInstance(result, str if not PY2 else unicode)
        self.assertEqual(target, result)

    def test_positional(self):
        """Test standard_repr with positional arguments."""
        self._helper('testreprutils.DummyClass()', [])
        self._helper('testreprutils.DummyClass(1)', [1])
        self._helper('testreprutils.DummyClass(1, 2, 3)', [1, 2, 3])

    def test_kwargs(self):
        """Test standard_repr with keyword arguments."""
        self._helper('testreprutils.DummyClass(arg=1)', kwargs=[('arg', 1)])
        self._helper('testreprutils.DummyClass(arg1=1, arg2=2, arg3=3)',
                     kwargs=[('arg1', 1), ('arg2', 2), ('arg3', 3)])
        self._helper('testreprutils.DummyClass(0, -1, arg=1)',
                     [0, -1], kwargs=[('arg', 1)])
        self._helper('testreprutils.DummyClass(0, 9, arg1=1, arg2=2, arg3=3)',
                     [0, 9], kwargs=[('arg1', 1), ('arg2', 2), ('arg3', 3)])

    def test_repr(self):
        """Assert the repr is being called on arguments."""
        # Built-in types
        self._helper('testreprutils.DummyClass(True, None, 4, 1.0)',
                     [True, None, 4, 1.0000000000000001])
        self._helper(
            'testreprutils.DummyClass(arg1=True, arg2=None, arg3=4, arg4=1.0)',
            kwargs=[('arg1', True), ('arg2', None), ('arg3', 4),
                    ('arg4', 1.0000000000000001)]
        )

        # Strings
        if PY2:
            self._helper("testreprutils.DummyClass(u'string', 'string')",
                         ['string', b'string'])
            self._helper(
                "testreprutils.DummyClass(arg1=u'string', arg2='string')",
                kwargs=[('arg1', 'string'), ('arg2', b'string')])

        else:
            self._helper("testreprutils.DummyClass('string', b'string')",
                         ['string', b'string'])
            self._helper(
                "testreprutils.DummyClass(arg1='string', arg2=b'string')",
                kwargs=[('arg1', 'string'), ('arg2', b'string')])

    def tearDown(self):
        """Remove the old dummy object."""
        del self.dc

class TestGetattrRepr(unittest.TestCase):
    """Test the GetattrRepr descriptor."""
    def setUp(self):
        """Create an instance of the dummy class."""
        self.dc = DummyClass()
        self.dc.a = 1
        self.dc.b = 2
        self.dc.c = 3
        self.dc.x = None
        self.dc.y = True
        self.dc.z = str('asdf')

    def tearDown(self):
        """Called after every test. Resets the __repr__ member."""
        del DummyClass.__repr__
        del self.dc

    def test_positional(self):
        """Test GetattrRepr with positional arguments."""
        DummyClass.__repr__ = GetattrRepr()
        self.assertEqual(repr(self.dc), 'testreprutils.DummyClass()')

        DummyClass.__repr__ = GetattrRepr('a')
        self.assertEqual(repr(self.dc), 'testreprutils.DummyClass(1)')

        DummyClass.__repr__ = GetattrRepr('a', 'b', 'c')
        self.assertEqual(repr(self.dc), 'testreprutils.DummyClass(1, 2, 3)')

    def test_kwargs(self):
        """Test standard_repr with keyword arguments."""
        # Standard kwarg
        DummyClass.__repr__ = GetattrRepr(arg='a')
        self.assertEqual('testreprutils.DummyClass(arg=1)', repr(self.dc))

        # Standard kwarg plus positionals
        DummyClass.__repr__ = GetattrRepr('a', 'b', arg='c')
        self.assertEqual('testreprutils.DummyClass(1, 2, arg=3)',
                         repr(self.dc))

        # Ordered kwarg
        DummyClass.__repr__ = GetattrRepr([('arg1', 'a')])
        self.assertEqual('testreprutils.DummyClass(arg1=1)', repr(self.dc))

        # Ordered kwargs
        DummyClass.__repr__ = GetattrRepr([('arg1', 'a'), ('arg2', 'b'),
                                           ('arg3', 'c')])
        self.assertEqual(
            'testreprutils.DummyClass(arg1=1, arg2=2, arg3=3)', repr(self.dc)
        )

        # Ordered kwargs plus positionals
        DummyClass.__repr__ = GetattrRepr(
            'x', 'y', [('arg1', 'a'), ('arg2', 'b'), ('arg3', 'c')]
        )
        self.assertEqual(
            'testreprutils.DummyClass(None, True, arg1=1, arg2=2, arg3=3)',
            repr(self.dc)
        )

        # Ordered kwargs plus positionals and unordered kwarg
        DummyClass.__repr__ = GetattrRepr(
            'x', 'y', [('arg1', 'a'), ('arg2', 'b'), ('arg3', 'c')], z='z'
        )
        self.assertEqual(
            "testreprutils.DummyClass(None, True, arg1=1, arg2=2, arg3=3, "
            "z='asdf')", repr(self.dc)
        )

        # Sugar ordered kwarg
        DummyClass.__repr__ = GetattrRepr(['a'])
        self.assertEqual('testreprutils.DummyClass(a=1)', repr(self.dc))

        # Sugar ordered kwargs
        DummyClass.__repr__ = GetattrRepr(['a', 'b', 'c'])
        self.assertEqual('testreprutils.DummyClass(a=1, b=2, c=3)',
                         repr(self.dc))

        # Sugar and regular ordered kwargs
        DummyClass.__repr__ = GetattrRepr(
            ['a', 'b', 'c', ('arg1', 'x'), ('arg2', 'y')]
        )
        self.assertEqual(
            'testreprutils.DummyClass(a=1, b=2, c=3, arg1=None, arg2=True)',
            repr(self.dc)
        )

        # Sugar and regular ordered kwargs with positional arguments
        DummyClass.__repr__ = GetattrRepr(
            'a', 'b', 'c', ['x', ('arg1', 'a'), 'y', ('arg2', 'b'),
                            ('arg3', 'c')]
        )
        self.assertEqual(
            repr(self.dc),
            "testreprutils.DummyClass(1, 2, 3, x=None, arg1=1, y=True, "
            "arg2=2, arg3=3)"
        )

        # Sugar and regular ordered kwargs with positional arguments and
        # an unordered kwarg
        DummyClass.__repr__ = GetattrRepr(
            'a', 'b', 'c', ['x', ('arg1', 'a'), 'y', ('arg2', 'b'),
                            ('arg3', 'c')], z='z'
        )
        self.assertEqual(
            repr(self.dc),
            "testreprutils.DummyClass(1, 2, 3, x=None, arg1=1, y=True, "
            "arg2=2, arg3=3, z='asdf')"
        )
