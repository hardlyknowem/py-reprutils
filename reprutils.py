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
import sys

PY2 = sys.version_info < (3,)

if PY2:
    from itertools import imap as map

__all__ = ['identifier', 'standard_repr', 'GetattrRepr']


def identifier(cls):
    """Return the fully-specified identifier of the class cls.

    @param cls: The class whose identifier is to be specified.

    """
    return cls.__module__ + '.' + cls.__name__


def standard_repr(obj, *args, **kwargs):
    """Return a repr-style string for obj, echoing and repring each argument.

    The output of this format follows the convention described in the
    module docstring: namely, the result will be a valid constructor for
    obj with a fully qualified path name, with the other positional and
    keyword arguments acting as arguments to the constructor.

    Note that repr, not str, will be called on each argument. This means
    that strings will be enclosed in quotation marks and escaped (which
    is exactly what one would expect).

    >>> class A(object):
    ...     pass
    >>> standard_repr(A(), 'mass\n', 45.3, 200, True, parent=None)
    __main__.A('mass\n', 45.3, 200, True, parent=None)

    @param obj: The object to be repr'ed.
    @param args: Positional arguments to appear in the repr.
    @param kwargs: Keyword arguments to appear in the repr.

    """
    parts = [identifier(obj.__class__), '(', ', '.join(map(repr, args))]

    has_items = bool(args)
    if kwargs:
        # Sort to get consistent behavior
        for key, value in sorted(kwargs.iteritems()):
            if has_items:
                parts.append(', ')
            parts.append(key)
            parts.append('=')
            parts.append(repr(value))
            has_items = True

    parts.append(')')

    return ''.join(parts)


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
    convenient. Every argument must be a str/bytes object, except the
    last, which may possibly be some non-str/bytes iterable. If it is
    not a str or bytes object, it will be iterated over and each item
    within will be inserted into kwargs as both a key and a value. This
    is to avoid repetitive code for which the name of a keyword
    parameter shares the same name as the instance attribute. This is
    perhaps better demonstrated by example. The following two lines of
    code are exactly equivalent:

    >>> GetattrRepr('pos1', 'pos2', kw1='kw1', kw2='kw2', kw3='kw3')
    >>> GetattrRepr('pos1', 'pos2', ['kw1', 'kw2', 'kw3'])

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
        self.args = args
        self.kwargs = kwargs

        if args and not isinstance(args[-1], six.string_types):
            kwargs.update((name, name) for name in args[-1])
            args = args[:-1]

        self.args = args
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        """Return this descriptor as a bound method.

        The method will be linked to this object's __call__ method.

        @param instance: The instance called by the object (or None if
            the attribute is being accessed by the class-level)
        @param owner: The class which defines the attribute.

        """
        return types.MethodType(self.__call__, instance, owner)

    def __call__(self, instance):
        """Return a standard representation of the object."""
        # my_getattr is a function with one argument `arg`.
        # It will return instance.<arg>
        my_getattr = functools.partial(getattr, instance)
        return standard_repr(
            instance, *(map(my_getattr, self.args)),
            **{k: my_getattr(v) for k, v in six.iteritems(self.kwargs)}
        )

    # Python 2 can't take unicode as __name__.
    # In Python 3, str is unicode, and is okay for __name__
    __call__.__name__ = str('__repr__')

