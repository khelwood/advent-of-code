#!/usr/bin/env python3

import sys
from itertools import combinations
from typing import NamedTuple

def between(v, a, b):
    return (a <= v <= b) if (a <= b) else (b <= v <= a)

class Line(NamedTuple):
    start: tuple
    end: tuple

    @property
    def x(self):
        return self.start[0]

    @property
    def y(self):
        return self.start[1]

    @property
    def horizontal(self):
        return self.start[1]==self.end[1]

    @property
    def vertical(self):
        return self.start[0]==self.end[0]

    def crosses(self, other):
        if self.horizontal:
            return (other.vertical and between(other.x, self.start[0], self.end[0])
                    and between(self.y, other.start[1], other.end[1]))
        else:
            return (other.horizontal and between(other.y, self.start[1], self.end[1])
                    and between(self.x, other.start[0], other.end[0]))
        return False

def read_input():
    lines = filter(bool, map(str.strip, sys.stdin))
    return [tuple(map(int, s.split(','))) for s in lines]

def rect_area(a,b):
    ax,ay = a
    bx,by = b
    return (abs(ax-bx)+1)*(abs(ay-by)+1)

def find_edges(points):
    last = points[-1]
    edges = []
    for cur in points:
        edges.append(Line(last, cur))
        last = cur
    return edges

def rect_corners(a,c):
    b = (a[0],c[1])
    d = (c[0],a[1])
    return (a,b,c,d)

def main():
    reds = read_input()
    print(max(rect_area(a,b) for (a,b) in combinations(reds, 2)))
    edges = find_edges(reds)
    best = 0
    for a,b in combinations(reds, 2):
        if a[0]==b[0] or a[1]==b[1]:
            continue
        area = rect_area(a,b)
        if area <= best:
            continue
        good = True
        sides = find_edges(rect_corners(a,b))
        xmin = min(a[0],b[0])
        xmax = max(a[0],b[0])
        ymin = min(a[1],b[1])
        ymax = max(a[1],b[1])
        for edge in edges:
            emin = tuple(min(edge.start[i], edge.end[i]) for i in (0,1))
            emax = tuple(max(edge.start[i], edge.end[i]) for i in (0,1))
            if (emax[0] <= xmin or emin[0] >= xmax or emax[1] <= ymin or emin[1] >= ymax):
                continue
            if any(side.crosses(edge) for side in sides):
                good = False
                break
        if good:
            best = area
    print(best)

if __name__ == '__main__':
    main()
