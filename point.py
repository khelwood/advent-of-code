#!/usr/bin/env python -tt

"""This module works in Python 2 or Python 3. It describes
a 2D point class called Point."""

__all__ = ['Point']

import operator
import sys

_PY = sys.version_info[0]

if _PY < 3:
    from itertools import izip as _zip
else:
    _zip = zip


def coordfn(fn):
    return lambda self, other: type(self)(fn(self[0], other[0]), fn(self[1], other[1]))
def scalarfn(fn):
    return lambda self, other: type(self)(fn(self[0], other), fn(self[1], other))

class Point(tuple):
    '2D immutable point class'
    __slots__ = ()
    def __new__(cls, x, y=None):
        if y is None:
            return tuple.__new__(cls, x)
        return tuple.__new__(cls, (x, y))
    x = property(lambda self: self[0], doc='Alias for field 0')
    y = property(lambda self: self[1], doc='Alias for field 1')
    __add__ = coordfn(operator.add)
    __radd__ = coordfn(lambda a,b: b+a)
    __sub__ = coordfn(operator.sub)
    __rsub__ = coordfn(lambda a,b: b-a)
    __str__ = tuple.__repr__
    def __repr__(self):
        return '%s%s'%(type(self).__name__, self)
    def __neg__(self):
        return Point(-self[0], -self[1])
    def __pos__(self):
        return self
    __mul__ = scalarfn(operator.mul)
    __rmul__ = scalarfn(lambda a,b: b*a)
    __floordiv__ = scalarfn(operator.floordiv)
    __truediv__ = scalarfn(operator.truediv)
    __mod__ = scalarfn(operator.mod)
    def dot(self, other):
        return sum(a*b for a,b in _zip(self, other))
    def __eq__(self, other):
        try:
            return (isinstance(other, tuple) and len(self)==len(other) and
                    all(a==b for a,b in _zip(self, other)))
        except TypeError:
            return False
    __hash__ = tuple.__hash__
    @classmethod
    def of(cls, p):
        return p if isinstance(p,cls) else cls(p[0], p[1])
    @classmethod
    def max(cls, *p):
        return cls(max(i[0] for i in p), max(i[1] for i in p))
    @classmethod
    def min(cls, *p):
        return cls(min(i[0] for i in p), min(i[1] for i in p))
    @classmethod
    def abs(cls, p):
        return cls(abs(p[0]), abs(p[1]))
    if _PY < 3:
        __div__ = scalarfn(operator.div)
        def __ne__(self, other):
            return not(self==other)
        __nonzero__ = any
    else:
        __bool__ = any

if __name__ == '__main__':
    p = Point(3,2)
    assert p==(3,2)
    assert p!=(2,3)
    assert p+p==(6,4)
    assert Point.of(p) is p
    assert Point.of((3,2))==p
    assert 2*p==p+p
    assert p/2==((1,1) if _PY < 3 else (1.5, 1.0))
    assert p//2==(1,1)
    assert -p==(-3,-2)
    assert Point.abs(-p)==p
    assert Point.min(p, -p)==-p
    assert Point.max(p, -p)==p
    assert p%2==(1,0)
