#!/usr/bin/env python3

import sys
from itertools import product

class Grid:
    def __init__(self, lines):
        self.lines = lines
    @property
    def width(self):
        return len(self.lines[0])
    @property
    def height(self):
        return len(self.lines)
    def __getitem__(self, p):
        x,y = p
        if (0 <= x < self.width and 0 <= y < self.height):
            return self.lines[y][x]
        return None

DIRS = tuple(d for d in product((-1,0,1), repeat=2) if any(d))

def addp(p,d):
    return (p[0]+d[0], p[1]+d[1])

def count_xmas(lines):
    grid = Grid(lines)
    count = 0
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='X':
                for d in DIRS:
                    p = (x,y)
                    for xc in 'MAS':
                        p = addp(p, d)
                        if grid[p]!=xc:
                            break
                    else:
                        count += 1
    return count


def has_crossmas(grid, p, MS=set('MS')):
    if grid[p]!='A':
        return False
    for dx in (-1,1):
        ca = grid[addp(p, (dx,1))]
        if ca not in MS:
            return False
        cb = grid[addp(p, (-dx,-1))]
        if cb not in MS or cb==ca:
            return False
    return True

def count_crossmas(lines):
    grid = Grid(lines)
    count = 0
    for p in product(range(1, grid.width-1), range(1, grid.height-1)):
        if has_crossmas(grid, p):
            count += 1
    return count


def main():
    lines = sys.stdin.read().strip().splitlines()
    print(count_xmas(lines))
    print(count_crossmas(lines))

if __name__ == '__main__':
    main()
