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

def coordfn(fn, swapped=False):
    if swapped:
        return lambda self, other: type(self)(fn(other[0], self[0]),
                                              fn(other[1], self[1]))
    return lambda self, other: type(self)(fn(self[0], other[0]),
                                          fn(self[1], other[1]))

def scalarfn(fn, swapped=False):
    if swapped:
        return lambda self, other: type(self)(fn(other, self[0]),
                                              fn(other, self[1]))
    return lambda self, other: type(self)(fn(self[0], other),
                                          fn(self[1], other))

class Point(tuple):
    '2D immutable point class'
    __slots__ = ()
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    x = property(operator.itemgetter(0), doc='Alias for field 0')
    y = property(operator.itemgetter(1), doc='Alias for field 1')
    __add__ = coordfn(operator.add)
    __radd__ = coordfn(operator.add, swapped=True)
    __sub__ = coordfn(operator.sub)
    __rsub__ = coordfn(operator.sub, swapped=True)
    def __str__(self):
        return '(%r,%r)'%self
    def __repr__(self):
        return type(self).__name__+str(self)
    def __neg__(self):
        return type(self)(-self[0], -self[1])
    def __pos__(self):
        return self
    __mul__ = scalarfn(operator.mul)
    __rmul__ = scalarfn(operator.mul, swapped=True)
    __floordiv__ = scalarfn(operator.floordiv)
    __truediv__ = scalarfn(operator.truediv)
    __mod__ = scalarfn(operator.mod)
    def dot(self, other):
        return sum(a*b for a,b in _zip(self, other))
    @classmethod
    def of(cls, p):
        return p if isinstance(p,cls) else cls(p[0], p[1])
    @classmethod
    def max(cls, *p):
        if len(p)==1:
            p = p[0]
        return cls(max(i[0] for i in p), max(i[1] for i in p))
    @classmethod
    def min(cls, *p):
        if len(p)==1:
            p = p[0]
        return cls(min(i[0] for i in p), min(i[1] for i in p))
    @classmethod
    def abs(cls, p):
        return cls(abs(p[0]), abs(p[1]))
    if _PY < 3:
        __div__ = scalarfn(operator.div)

if __name__ == '__main__':
    p = Point(3,2)
    assert p==(3,2)
    assert p is +p
    assert p!=(2,3)
    assert p+p==(6,4)
    assert Point.of(p) is p
    assert Point.of((3,2))==p
    assert 2*p==p+p==p*2
    assert p/2==((1,1) if _PY < 3 else (1.5, 1.0))
    assert p//2==(1,1)
    assert p/2.0==(1.5, 1.0)
    assert -p==(-3,-2)
    assert Point.abs(-p)==p
    assert Point.min(p, -p)==-p
    assert Point.max(p, -p)==p
    assert p%2==(1,0)
    assert Point.max([p,-p])==p
    assert Point.min([p,-p])==-p
    assert bool(Point(0,1))
    assert bool(Point(1,0))
    assert bool(Point(0,0))
    assert hash((1,2))==hash(Point(1,2))
    assert p-(0,1)==(3,1)
    assert (5,5)-p==(2,3)
    assert p+(0,1)==(3,3)==(0,1)+p
    assert p.x==3
    assert p.y==2
    assert p.dot((3,4))==17
    assert str(p)=='(3,2)'
    assert repr(p)=='Point(3,2)'
