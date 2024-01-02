#!/usr/bin/env python3

import sys

from dataclasses import dataclass
from itertools import cycle
from collections import Counter

NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def negp(a):
    return (-a[0], -b[0])

def subp(a,b):
    return (a[0]-b[0], a[1]-b[1])

def make_candidates(d):
    p = (d[1], -d[0])
    return (d, addp(d,p), subp(d,p))

CANDIDATES = {d:make_candidates(d) for d in (NORTH, SOUTH, WEST, EAST)}

@dataclass
class Elf:
    pos: tuple
    proposed: tuple = None

    def any_nearby(self, grid):
        sx,sy = self.pos
        return (any((x,sy-1) in grid for x in (sx-1,sx,sx+1))
            or any((x,sy+1) in grid for x in (sx-1,sx,sx+1))
            or (sx-1,sy) in grid or (sx+1,sy) in grid)

    def propose(self, grid, direcs):
        p = None
        if self.any_nearby(grid):
            for direc in direcs:
                if all(addp(self.pos, d) not in grid for d in CANDIDATES[direc]):
                    p = addp(self.pos, direc)
                    break
        self.proposed = p
        return p


def read_grid(lines):
    grid = {}
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                grid[x,y] = Elf((x,y))
    return grid

def perform_round(grid, direcs):
    c = Counter()
    any_moved = False
    for elf in grid.values():
        p = elf.propose(grid, direcs)
        if p:
            c[p] += 1
    for elf in list(grid.values()):
        if elf.proposed and c[elf.proposed]==1:
            del grid[elf.pos]
            grid[elf.proposed] = elf
            elf.pos = elf.proposed
            any_moved = True
    return any_moved

def find_bounds(grid):
    ps = iter(grid)
    x0,y0 = x1,y1 = next(ps)
    for x,y in ps:
        x0 = min(x,x0)
        y0 = min(y,y0)
        x1 = max(x,x1)
        y1 = max(y,y1)
    return (x0,y0), (x1,y1)

def draw_grid(grid):
    (x0,y0), (x1,y1) = find_bounds(grid)
    xran = range(x0, x1+1)
    print(f'   {x0}')
    for y in range(y0, y1+1):
        print(f'{y:>2} '+''.join('#' if (x,y) in grid else '.' for x in xran))
    print()

def main():
    lines = sys.stdin.read().strip().splitlines()
    cands = list(CANDIDATES)
    all_direcs = tuple(tuple(cands[i%4] for i in range(j, j+4)) for j in range(4))
    all_direcs = cycle(all_direcs)
    grid = read_grid(lines)
    for _ in range(10):
        perform_round(grid, next(all_direcs))
    p0,p1 = find_bounds(grid)
    w,h = (p1[i]+1-p0[i] for i in (0,1))
    print("Part 1:", w*h - len(grid))
    turns = 11
    while perform_round(grid, next(all_direcs)):
        turns += 1
    print("Part 2:", turns)

if __name__ == '__main__':
    main()
