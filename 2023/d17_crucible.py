#!/usr/bin/env python3

import sys

from itertools import product
from typing import NamedTuple
from collections import defaultdict

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def left(p):
    return (p[1], -p[0])

def right(p):
    return (-p[1], p[0])


NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

VERTICAL = (NORTH, SOUTH)
HORIZONTAL = (EAST, WEST)

DIRECTIONS = VERTICAL + HORIZONTAL

class Grid:
    def __init__(self, lines):
        self.lines = tuple(tuple(map(int, line)) for line in lines)

    def init_steps(self, min_step, max_step):
        self.next_steps = {
           pd: list(next_steps(self, pd, min_step, max_step))
           for pd in product(self, (HORIZONTAL, VERTICAL))
        }

    @property
    def wid(self):
        return len(self.lines[0])

    @property
    def hei(self):
        return len(self.lines)

    def __getitem__(self, p):
        x,y = p
        return self.lines[y][x]

    def __iter__(self):
        return ((x,y) for y,x in product(range(self.hei), range(self.wid)))

    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)


# A step is N moves in a direction perpendicular to the previous
def next_steps(grid, pd, min_step, max_step):
    pos, last_dir = pd
    newdir = HORIZONTAL if last_dir is VERTICAL else VERTICAL
    for d in newdir:
        q = pos
        heat = 0
        for step in range(1, max_step+1):
            q = addp(q,d)
            if q not in grid:
                break
            heat += grid[q]
            if step >= min_step:
                yield (q,newdir,heat)

def basic_route_heat(grid, min_step, max_step):
    heat = 0
    ex = grid.wid-1
    ey = grid.hei-1
    x = y = 0
    while x <= ex-min_step and y <= ey-min_step:
        for _ in range(min_step):
            x += 1
            heat += grid[x,y]
        for _ in range(min_step):
            y += 1
            heat += grid[x,y]
    while x < ex:
        x += 1
        heat += grid[x,y]
    while y < ey:
        y += 1
        heat += grid[x,y]
    return heat

def find_routes(grid, start, min_step, max_step):
    grid.init_steps(min_step, max_step)
    new = [(start, HORIZONTAL, 0), (start, VERTICAL, 0)]
    routes = {}
    BIG = basic_route_heat(grid, min_step, max_step)
    def sort_key(pdh):
        return pdh[2]
    while new:
        old = new
        old.sort(key=sort_key)
        new = []
        for (p,d,heat) in old:
            pd = (p,d)
            if routes.get(pd, BIG) <= heat:
                continue
            routes[pd] = heat
            for q,d,dh in grid.next_steps[pd]:
                h = heat + dh
                if routes.get((q,d), BIG) > h:
                    new.append((q,d,h))
    return routes

def main():
    grid = Grid(sys.stdin.read().strip().splitlines())
    start = (0,0)
    end = (grid.wid-1, grid.hei-1)
    for (part, (min_step, max_step)) in enumerate(((1,3), (4,10)), 1):
        routes = find_routes(grid, start, min_step, max_step)
        heat = min(routes.get((end,d), 10_000) for d in (VERTICAL, HORIZONTAL))
        print(f"Part {part}: {heat}")

if __name__ == '__main__':
    main()
