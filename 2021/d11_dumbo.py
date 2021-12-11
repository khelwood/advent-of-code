#!/usr/bin/env python3

import sys

DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1))

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def read_grid():
    grid = {}
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            grid[x,y] = int(ch)
    return grid

def neighbours(p):
    return (addp(p,d) for d in DIRECTIONS)

def advance(grid) -> int:
    for p,n in grid.items():
        grid[p] = n+1
    flashes = set()
    more = True
    while more:
        more = False
        for p in grid:
            if grid[p] > 9 and p not in flashes:
                flashes.add(p)
                more = True
                for r in neighbours(p):
                    if r in grid:
                        grid[r] += 1
    for p in flashes:
        grid[p] = 0
    return len(flashes)

def main():
    initial_grid = read_grid()
    grid = dict(initial_grid)
    num_flashes = 0
    for _ in range(100):
        num_flashes += advance(grid)
    print("Num flashes:", num_flashes)
    grid = dict(initial_grid)
    size = len(grid)
    count = 1
    while advance(grid) < size:
        count += 1
    print("Steps till sync:", count)

if __name__ == '__main__':
    main()
