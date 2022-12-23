#!/usr/bin/env python3

import sys
from ast import literal_eval as leval

DIRECTIONS = ((0,1), (-1,1), (1,1))
ROCK = '#'
SAND = 'o'
START = (500,0)

def direc(a,b):
    ax,ay = a
    bx,by = b
    if ax==bx:
        return (0, (1 if ay < by else -1))
    if ay==by:
        return ((1 if ax < bx else -1), 0)
    raise ValueError(f"Not in line: {a,b}")

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def read_input():
    for line in sys.stdin:
        line = line.strip()
        points = line.split(' -> ')
        points = list(map(leval, points))
        yield points

def build_grid(lines):
    grid = {}
    for line in lines:
        last = None
        for p in line:
            grid[p] = ROCK
            if last is None:
                last = p
            else:
                d = direc(last, p)
                while last != p:
                    last = addp(last, d)
                    grid[last] = ROCK
    return grid

def track_sand(grid, abyss, start=START):
    count = 0
    while sand_fall(grid, start, abyss):
        count += 1
    return count

def sand_fall(grid, start, abyss, floor=None, dirs=DIRECTIONS):
    p = start
    while p[1] < abyss:
        for d in dirs:
            q = addp(p, d)
            if q not in grid:
                p = q
                break
        else:
            grid[p] = SAND
            return True
    return False

def track_sand_floor(grid, floor, start=START):
    count = 0
    while sand_fall_floor(grid, start, floor):
        count += 1
    return count

def sand_fall_floor(grid, start, floor, dirs=DIRECTIONS):
    if start in grid:
        return False
    p = start
    while True:
        for d in dirs:
            q = addp(p,d)
            if q[1] < floor and q not in grid:
                p = q
                break
        else:
            grid[p] = SAND
            return True

def render(grid):
    x0,y0 = START
    x1,y1 = START
    for x,y in grid:
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)
    for y in range(y0, y1+1):
        print()
        for x in range(x0, x1+1):
            v = grid.get((x,y), '.')
            print(v, end='')
    print()

def main():
    lines = list(read_input())
    grid = build_grid(lines)
    abyss = max(y for (x,y) in grid)
    num = track_sand(grid, abyss)
    print("Num sand:", num)
    grid = {k:v for (k,v) in grid.items() if v==ROCK}
    num = track_sand_floor(grid, abyss+2)
    print("Num sand:", num)
    # render(grid)

if __name__ == '__main__':
    main()
