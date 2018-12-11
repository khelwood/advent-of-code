#!/usr/bin/env python3

import sys
import itertools

sys.path.append('..')
from grid import Grid

def make_grid(serial, width=300, height=300):
    grid = Grid(width+1, height+1, fill=' ')
    for x in range(1, width+1):
        rackid = x+10
        for y in range(1, height+1):
            power = rackid * (rackid * y + serial)
            grid[x,y] = (power//100)%10 - 5
    return grid

def group_total(grid, x, y):
    return sum(grid[p] for p in itertools.product(range(x, x+3), range(y, y+3)))

def high_spot(grid):
    yran = range(1, grid.height-2)
    best_total = -100
    for (x,y) in itertools.product(
            range(1, grid.width-2),
            range(1, grid.height-2)
        ):
        total = group_total(grid, x, y)
        if total > best_total:
            best_total = total
            best = (x,y)
    return best

def main():
    serial = int(sys.argv[1])
    grid = make_grid(serial)
    x,y = high_spot(grid)
    print("High spot:", (x,y))
    print("with group power", group_total(grid, x, y))

if __name__ == '__main__':
    main()
