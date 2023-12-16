#!/usr/bin/env python3

import sys

from dataclasses import dataclass
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self[0]+other[0], self[1]+other[1])

Point.UP = Point(0,-1)
Point.LEFT = Point(-1,0)
Point.RIGHT = Point(1,0)
Point.DOWN = Point(0,1)

@dataclass(frozen=True)
class Ray:
    pos: Point
    dir: Point

@dataclass(frozen=True)
class Grid:
    wid: int
    hei: int
    mirrors: dict

    def __getitem__(self, pos):
        return self.mirrors.get(pos, '.')

    def __contains__(self, pos):
        x,y = pos
        return (0 <= x < self.wid and 0 <= y < self.hei)

def split_dash(d):
    if d[0]:
        return (d,)
    return (Point.LEFT, Point.RIGHT)

def split_pipe(d):
    if d[1]:
        return (d,)
    return (Point.UP, Point.DOWN)

MIRROR_OP = {
   '/': lambda p: (Point(-p[1], -p[0]),),
   '\\': lambda p: (Point(p[1], p[0]),),
   '-': split_dash,
   '|': split_pipe,
}

def read_mirrors(lines):
    mirrors = {}
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch!='.':
                mirrors[Point(x,y)] = ch
    return Grid(len(lines[0]), len(lines), mirrors)

def trace_beam(grid, start):
    all_rays = set()
    new = {start}
    while new:
        all_rays |= new
        old = new
        new = set()
        for ray in old:
            v = grid[ray.pos]
            if v=='.':
                q = ray.pos + ray.dir
                if q in grid:
                    qr = Ray(q, ray.dir)
                    if qr not in all_rays:
                        new.add(qr)
                continue
            qds = MIRROR_OP[v](ray.dir)
            for qd in qds:
                q = ray.pos + qd
                if q in grid:
                    qr = Ray(q, qd)
                    if qr not in all_rays:
                        new.add(qr)
    return all_rays

def count_energised(grid, start):
    rays = trace_beam(grid, start)
    energised = set(ray.pos for ray in rays)
    return len(energised)

def starts(grid):
    for x in range(grid.wid):
        yield Ray(Point(x,0), Point.DOWN)
        yield Ray(Point(x,grid.hei-1), Point.UP)
    for y in range(grid.hei):
        yield Ray(Point(0,y), Point.RIGHT)
        yield Ray(Point(grid.wid-1,y), Point.LEFT)

def main():
    lines = sys.stdin.read().strip().splitlines()
    grid = read_mirrors(lines)
    start = Ray(Point(0,0), Point.RIGHT)
    print("Part 1:", count_energised(grid, start))
    best = max(count_energised(grid, start) for start in starts(grid))
    print("Part 2:", best)

if __name__ == '__main__':
    main()
