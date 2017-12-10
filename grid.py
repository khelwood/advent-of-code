#!/usr/bin/env python2.7 -tt

from point import Point
import sys

_PY = sys.version_info[0]

if _PY < 3:
    _range = xrange
else:
    _range = range

class Grid(object):
    def __init__(self, width, height, fill=None):
        self._width = width
        self._height = height
        self._data = [fill]*(width*height)
    width = property(lambda self : self._width)
    height = property(lambda self : self._height)
    def copy(self):
        cp = Grid.__new__(type(self))
        cp._width = self.width
        cp._height = self.height
        cp._data = self._data[:]
        return cp
    def len(self):
        return len(self._data)
    def __iter__(self):
        return iter(self._data)
    def _toindex(self, x,y=None):
        if y is None:
            x,y = x
        if (x,y) not in self:
            raise ValueError("Coordinates outside grid: %s"%((x,y),))
        return x + self.width*y
    def _toxy(self, index):
        if not 0 <= index < len(self):
            raise ValueError("Index outside grid: %s"%index)
        return Point(index%self.width, index//self.width)
    def __contains__(self, p):
        return (0 <= p[0] < self.width
                and 0 <= p[1] < self.height)
    def __getitem__(self, p):
        return self._data[self._toindex(p)]
    def __setitem__(self, p, v):
        self._data[self._toindex(p)] = v
    def __delitem__(self, p):
        self._data[self._toindex(p)] = None
    def getrow(self, y):
        return self._data[self._toindex(0,y) : self._toindex(self.width-1,y)+1]
    def getcolumn(self, x):
        return self._data[self._toindex(x,0) :
                          self._toindex(x, self.height-1)+1 :
                          self.width]
    def rows(self):
        for y in _range(self.height):
            yield self.getrow(y)
    def columns(self):
        for x in _range(self.width):
            yield self.getcolumn(x)
    def __eq__(self, other):
        if self is other:
            return True
        if type(other) is not type(self):
            return False
        return (self._width==other._width and self._height==other._height
                and self._data==other._data)
    def __ne__(self, other):
        return not(self==other)
    def __str__(self):
        return '\n'.join([' '.join([str(x) for x in row])
                         for row in self.rows()])
