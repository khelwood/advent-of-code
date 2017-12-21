#!/usr/bin/env python2.7 -tt

from point import Point
import sys
import itertools

_PY = sys.version_info[0]

if _PY < 3:
    _range = xrange
else:
    _range = range

class Grid(object):
    def __init__(self, width, height, fill=None):
        self._width = width
        self._height = height
        self._rows = [[fill]*width for _ in _range(height)]
    width = property(lambda self : self._width)
    height = property(lambda self : self._height)
    def copy(self):
        cp = Grid.__new__(type(self))
        cp._width = self.width
        cp._height = self.height
        cp._rows = [row[:] for row in self._rows]
        return cp
    def __len__(self):
        return (self.width*self.height)
    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Point(x,y)
    def __contains__(self, p):
        return (0 <= p[0] < self.width
                and 0 <= p[1] < self.height)
    def __getitem__(self, p):
        return self._rows[p[1]][p[0]]
    def __setitem__(self, p, value):
        self._rows[p[1]][p[0]] = value
    def __delitem__(self, p):
        self._rows[p[1]][p[0]] = None
    def rows(self):
        return self._rows
    def values(self):
        return itertools.chain(*self._rows)
    def count(self, value):
        return sum(row.count(value) for row in self._rows)
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
