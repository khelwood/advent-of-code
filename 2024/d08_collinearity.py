#!/usr/bin/env python3

import sys
import math
from collections import defaultdict
from itertools import permutations, combinations

class Point(tuple):
    @classmethod
    def at(cls, x, y):
        return cls((x,y))
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self, p))
    def __sub__(self, p):
        return Point(a-b for (a,b) in zip(self, p))
    def __neg__(self):
        return Point(-a for a in self)
    def __mul__(self, s):
        return Point(a*s for a in self)
    __rmul__ = __mul__
    def __intdiv__(self, d):
        return Point(a//d for a in self)
    def reduce(self):
        d = math.gcd(*self)
        return self if d==1 else self//d

class Grid:
    def __init__(self, nodes, wid, hei):
        self.nodes = nodes
        self.wid = wid
        self.hei = hei
    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)

def read_grid():
    nodes = defaultdict(list)
    for y,line in enumerate(filter(bool, map(str.strip, sys.stdin))):
        for x,ch in enumerate(line):
            if ch!='.':
                nodes[ch].append(Point.at(x,y))
    return Grid(nodes, x+1, y+1)

def find_antinodes_1(grid):
    antinodes = set()
    for groups in grid.nodes.values():
        for (a,b) in permutations(groups, 2):
            c = 2*a - b
            if c in grid:
                antinodes.add(c)
    return antinodes

def find_antinodes_2(grid):
    antinodes = set()
    for groups in grid.nodes.values():
        for (a,b) in combinations(groups, 2):
            d = (b-a).reduce()
            p = a
            while p in grid:
                antinodes.add(p)
                p += d
            p = a - d
            while p in grid:
                antinodes.add(p)
                p -= d
    return antinodes


def main():
    grid = read_grid()
    antinodes = find_antinodes_1(grid)
    print(len(antinodes))
    antinodes = find_antinodes_2(grid)
    print(len(antinodes))

if __name__ == '__main__':
    main()
