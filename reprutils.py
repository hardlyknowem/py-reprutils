"""This module contains utilities for creating standardized reprs.

Python objects may define a method, `__repr__`, which is called whenever
the builtin function `repr` is called with the object as an argument.
It is most commonly used by the interactive interperter (or the pdb
interpreter), which uses `repr` to print the return value of any
interactive expression. For that reason, `__repr__` is generally used in
debugging contexts.

The returned object must be a string, and by convention most objects
define `__repr__` in such a way that if the return value were passed as
an argument to `eval`, it would return an equivalent object. While I do
not know of any Python code that actually takes advantage of the
behavior (and even for objects whose `__repr__` follow the `eval`
convention, I would expect the behavior to fail in most cases because
of differences in namespace conventions), it is useful in debugging
sessions with the interactive

Designing a `__repr__` method to meet the preceding convention is a
repetitive task, and so this module contains tools to save some tedious
work. Generally, you want to return a string containing the fully
qualified identifier (i.e., full package and name of the class) followed
by a pair of parenthesis, inside of which a few instance attributes will
be placed. (This has the effect of printing out a valid constructor for
the object).

Most users will want to make use of make_repr, which will create a
curried function.

Example usage:

>>> class MyClass(object):
...     def __init__(self, name, value, units=None):
...         self.name = name
...         self.value = value
...         self.units = units
...
...     __repr__ = GetattrRepr('name', 'value', ['units'])
...
...
>>> my_object1 = MyClass('counts', 400)
>>> my_object2 = MyClass('mass', 45.3, 'kilograms')
>>> repr(my_object1)
__main__.MyClass('counts', 400, units=None)
>>> repr(my_object2)
__main__.MyClass('mass', 45.3, units='kilograms')

Author: Matthew Lefavor
Email:  matthew.lefavor@nasa.gov
Date:   2013-02-06

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import functools
import types
import itertools
import sys

PY2 = sys.version_info < (3,)

if PY2:
    from itertools import imap as map
    string_base = basestring
    iteritems = dict.iteritems
else:
    string_base = str
    iteritems = dict.items

__all__ = ['identifier', 'standard_repr', 'GetattrRepr']


def identifier(cls):
    """Return the fully-specified identifier of the class cls.

    @param cls: The class whose identifier is to be specified.

    """
    return cls.__module__ + '.' + cls.__name__


def standard_repr(obj, args=None, kwargs=None):
    """Return a repr-style string for obj, echoing and repring each argument.

    The output of this format follows the convention described in the
    module docstring: namely, the result will be a valid constructor for
    obj with a fully qualified path name, with the other positional and
    keyword arguments acting as arguments to the constructor.

    The first argument is a reference to the object of which the result
    should be a representation. The second argument is a list of values
    to appear as positional arguments in the repr. (These should be
    actual values and not already converted to repr-ized strings). The
    final argument should be a list of (kwarg, value) tuples which will
    appear in the repr as positional arguments, in that order.

    This unwieldy argument syntax is necessary to ensure that the
    keyword arguments are ordered properly. (This used to accept *args
    and **kwargs, but the ordering of keyword arguments is arbitrary in
    that case.)

    Note that repr (not str) will be called on each argument. This means
    that strings will be enclosed in quotation marks and escaped in the
    result (which is exactly what one would expect).

    >>> class A(object):
    ...     pass
    >>> standard_repr(A(), ['mass\n', 45.3, 200, True], [('parent', None)])
    __main__.A('mass\n', 45.3, 200, True, parent=None)

    @param obj: The object to be repr'ed.
    @param args: Positional arguments to appear in the repr.
    @param kwargs: A list of (kwarg, value) tuples. The `kwarg` element
        must be a string.

    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []

    if not all(isinstance(tpl[0], string_base) for tpl in kwargs):
        raise TypeError('kwarg names must be strings')

    items = itertools.chain(
        map(repr, args),
        ('{0}={1!r}'.format(kwarg, value) for kwarg, value in kwargs),
    )

    return ''.join([identifier(obj.__class__), '(', ', '.join(items), ')'])


class GetattrRepr(object):
    """A descriptor to assign to a class's __repr__ attribute.

    Consider some class C to which a GetattrRepr is assigned as the
    class's `__repr__` attribute, and obj which is an instance of C. For
    each argument arg passed to GetattrRepr's constructors, the value of
    repr(getattr(obj, arg)) will apear as a positional argument in the
    final output. For each keyword argument k with value v, the keyword
    argument pair k=repr(getattr(obj, v) will appear in the final output
    of the repr.

    >>> class MyClass(object):
    ...     def __init__(self, name, value, units=None):
    ...         self.name = name
    ...         self.value = value
    ...         self.units = units
    ...
    ...     __repr__ = GetattrRepr('name', 'value', units='units')
    ...
    ...
    >>> my_object1 = MyClass('counts', 400)
    >>> my_object2 = MyClass('mass', 45.3, 'kilograms')
    >>> repr(my_object1)
    __main__.MyClass('counts', 400, units=None)
    >>> repr(my_object2)
    __main__.MyClass('mass', 45.3, units='kilograms')

    There is one further subtlety to make it more syntactically
    convenient. Every positional argument must be a str/bytes object,
    except the last, which may possibly be some other kind of iterable.
    If it is not a str or bytes object, it will be iterated over. For
    each item that is a tuple, it will be assumed that the first item
    is the name of the keyword parameter and the second item is the
    attribute name that should be called. For each item that is not a
    tuple, it will be assumed to be both the name of the parameter and
    the name of the attribute. This is done to allow for repeatable
    ordering of keyword arguments. The handling of non-tuple arguments
    is pure sugar to avoid repetitive typing. Any keyword arguments
    that are also passed to the function will appear in the resulting
    repr in arbitrary order, after any keyword arguments specified in
    this manner.

    The following are all equivalent (with the exception of the way
    keywords are ordered in the first example, which depends on the
    python implementation):

    >>> GetattrRepr('pos1', 'pos2', kw1='kw1', kw2='kw2', kw3='kw3')
    >>> GetattrRepr('pos1', 'pos2', ['kw1', 'kw2', 'kw3'])
    >>> GetattrRepr('pos1', 'pos2', [('kw1', 'kw1'), ('kw2', 'kw2'),
    ...                              ('kw3', 'kw3')])
    >>> GetattrRepr('pos1', 'pos2', ['kw1', ('kw2', 'kw2')], kw3='kw3')

    """
    def __init__(self, *args, **kwargs):
        """Initialize the GetattrRepr descriptor.

        @param args: The names of attributes to be included as
            positional arguments in the repr, with the possible
            exception of the last argument as described in the class
            docstring.
        @param kwargs: The keyword names to appear in the repr and the
            associated names of attributes to appear as values.

        """
        if args and not isinstance(args[-1], string_base):
            self.args = args[:-1]
            self.kwargs = [
                item if not isinstance(item, string_base) else (item, item)
                for item in args[-1]
            ]
            self.kwargs.extend(iteritems(kwargs))
        else:
            self.args = args
            self.kwargs = list(iteritems(kwargs))

    def __get__(self, instance, owner):
        """Return this descriptor as a bound method.

        The method will be linked to this object's __call__ method.

        @param instance: The instance called by the object (or None if
            the attribute is being accessed by the class-level)
        @param owner: The class which defines the attribute.

        """
        if instance is None:
            return self

        return types.MethodType(self.__call__, instance)

    def __call__(self, instance):
        """Return a standard representation of the object."""
        # my_getattr is a function with one argument `arg`.
        # It will return instance.<arg>
        my_getattr = functools.partial(getattr, instance)
        return standard_repr(
            instance, list(map(my_getattr, self.args)),
            [(k, my_getattr(v)) for k, v in self.kwargs]
        )

    # Python 2 can't take unicode as __name__.
    # In Python 3, str is unicode, and is okay for __name__
    __call__.__name__ = str('__repr__')

