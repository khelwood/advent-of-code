#!/usr/bin/env python -tt

"""This module works in Python 2 or Python 3. It describes
a 2D point class called Point."""

__all__ = ['Point']

import sys

_PY = sys.version_info[0]

class Point(tuple):
    '2D immutable point class'
    __slots__ = ()
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    x = property(lambda self: self[0], doc='Alias for field 0')
    y = property(lambda self: self[1], doc='Alias for field 1')
    def __add__(self, other):
        return type(self)(self[0]+other[0], self[1]+other[1])
    def __radd__(self, other):
        return type(self)(other[0]+self[0], other[1]+self[1])
    def __sub__(self, other):
        return type(self)(self[0]-other[0], self[1]-other[1])
    def __rsub__(self, other):
        return type(self)(other[0]-self[0], other[1]-self[1])
    def __str__(self):
        return '(%r,%r)'%self
    def __repr__(self):
        return type(self).__name__+str(self)
    def __neg__(self):
        return type(self)(-self[0], -self[1])
    def __pos__(self):
        return self
    def __mul__(self, other):
        return type(self)(self[0]*other, self[1]*other)
    def __rmul__(self, other):
        return type(self)(other*self[0], other*self[1])
    def __floordiv__(self, other):
        return type(self)(self[0]//other, self[1]//other)
    def __truediv__(self, other):
        return type(self)(self[0]/other, self[1]/other)
    def __mod__(self, other):
        return type(self)(self[0]%other, self[1]%other)
    def dot(self, other):
        return (self[0]*other[0] + self[1]*other[1])
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
        def __div__(self, other):
            return type(self)(self[0]/other, self[1]/other)

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
