#!/usr/bin/env python3

import sys
from itertools import product

class Point(tuple):
    @classmethod
    def of(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for a,b in zip(self,p))
    def __sub__(self, p):
        return Point(a-b for a,b in zip(self,p))
    def __neg__(self):
        return Point(-a for a in self)
    def rotate(self):
        return Point.of(-self[1], self[0])

UP = Point.of(0,-1)
RIGHT = Point.of(1,0)
DOWN = Point.of(0,1)
LEFT = Point.of(-1,0)
DIRECTIONS = (UP,RIGHT,DOWN,LEFT)

class Garden:
    def __init__(self, lines):
        self.lines = lines
    def __getitem__(self, p):
        if p not in self:
            return None
        x,y = p
        return self.lines[y][x]
    @property
    def width(self):
        return len(self.lines[0])
    @property
    def height(self):
        return len(self.lines)
    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.width and 0 <= y < self.height)
    def __iter__(self):
        return map(Point, product(range(self.width), range(self.height)))

def read_garden():
    return Garden(sys.stdin.read().strip().splitlines())

def find_regions(garden):
    regions = []
    done = set()
    for p in garden:
        if p not in done:
            region = find_region(garden, p)
            regions.append(region)
            done.update(region)
    return regions

def find_region(garden, p):
    """Flood fill from point p, using a set to mark the filled points."""
    region = set()
    v = garden[p]
    stack = [p]
    while stack:
        p = stack.pop()
        if p in region or garden[p]!=v:
            continue
        for (r, rd) in ((p, RIGHT), (p+LEFT, LEFT)):
            while garden[r]==v and r not in region:
                region.add(r)
                for q in (r+ud for ud in (UP,DOWN)):
                    if q not in region and garden[q]==v:
                        stack.append(q)
                r += rd
    return region

def perimeter(region):
    return sum((p+d) not in region for p in region for d in DIRECTIONS)

def find_sides(region):
    sides = []
    done = set()
    for p in region:
        for d in DIRECTIONS:
            if (p,d) in done or (p+d) in region:
                continue
            side = scan_side(region, p, d)
            sides.append(side)
            for s in side:
                done.add((s,d))
    return sides

def scan_side(region, p, d):
    side = set()
    pd = d.rotate()
    for (q,qd) in ((p,pd), (p-pd,-pd)):
        while q in region and (q+d) not in region:
            side.add(q)
            q += qd
    return side

def main():
    garden = read_garden()
    regions = find_regions(garden)
    cost1 = sum(len(region)*perimeter(region) for region in regions)
    print(cost1)
    cost2 = sum(len(region)*len(find_sides(region)) for region in regions)
    print(cost2)


if __name__ == '__main__':
    main()
