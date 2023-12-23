#!/usr/bin/env python3

import sys

from typing import NamedTuple

ROCK = '#'
PLOT = '.'

NORTH = (0,-1)
SOUTH = (0,1)
WEST = (-1,0)
EAST = (1,0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

class Maze:
    def __init__(self, wid, hei, start, rocks):
        self.wid = wid
        self.hei = hei
        self.start = start
        self.rocks = rocks
        self._cache = {}

    def is_rock(self, p):
        return p in self.rocks

    def __getitem__(self, p):
        return ROCK if self.is_rock(p) else PLOT

    def is_plot(self, p):
        return p in self and not self.is_rock(p)

    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)

    def neighbours(self, p):
        cache = self._cache
        nbrs = cache.get(p)
        if nbrs is not None:
            return nbrs
        nbrs = cache[p] = set()
        for d in DIRECTIONS:
            q = addp(p,d)
            if self.is_plot(q):
                nbrs.add(q)
        return nbrs

    @classmethod
    def read(cls, lines):
        rocks = set()
        for y,line in enumerate(lines):
            for x,ch in enumerate(line):
                if ch==ROCK:
                    rocks.add((x,y))
                elif ch=='S':
                    start = (x,y)
        return cls(len(lines[0]), len(lines), start, rocks)

class InfiniteMaze(Maze):
    def is_rock(self, p):
        x,y = p
        x %= self.wid
        y %= self.hei
        return (x,y) in self.rocks

    def is_plot(self, p):
        return not self.is_rock(p)

    def directions(self, p):
        x,y = p
        x %= self.wid
        y %= self.hei
        cache = self._cache
        ds = cache.get((x,y))
        if ds is not None:
            return ds
        ds = cache[p] = [d for d in DIRECTIONS if not self.is_rock(addp(d,p))]
        return ds

    def neighbours(self, p):
        return {addp(p,d) for d in self.directions(p)}


def find_destinations(maze, steps):
    positions = {maze.start}
    while steps > 0:
        steps -= 1
        old = positions
        positions = set()
        for pos in old:
            positions |= maze.neighbours(pos)
    return positions

def measure(maze: InfiniteMaze, target: int):
    # 26501365 % 131 is 65.
    # Find answer for (65 + n*131) for a few values of n.
    # Notice that it is quadratic (2nd order differences are constant).
    # Use the points we've worked out to find quadratic coefficients.
    mup = target%131
    positions = {maze.start}
    for step in range(1, 131*4+mup+1):
        old = positions
        positions = set()
        for pos in old:
            positions |= maze.neighbours(pos)
        if step%131==mup:
            print("step:", step, "\tsquares:", len(positions))


def calculate_spaces(n): # based on my data
    return (15287*n**2 + 28518*n + 40469)//17161

def main():
    lines = sys.stdin.read().strip().splitlines()
    maze = Maze.read(lines)
    dests = find_destinations(maze, 64)
    print("Part 1:", len(dests))
    # measure(InfiniteMaze.read(lines), 26501365)
    print("Part 2:", calculate_spaces(26501365))


if __name__ == '__main__':
    main()
