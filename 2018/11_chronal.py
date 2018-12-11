#!/usr/bin/env python3

import sys
import itertools

sys.path.append('..')
from grid import Grid

def make_grid(serial, width=300, height=300):
    grid = Grid(width+1, height+1)
    for x in range(1, width+1):
        rackid = x+10
        for y in range(1, height+1):
            power = rackid * (rackid * y + serial)
            grid[x,y] = (power//100)%10 - 5
    return grid

def make_sum_grid(grid):
    sg = Grid(grid.width, grid.height, fill=0)
    for (x,y) in itertools.product(
            range(1, grid.width),
            range(1, grid.height)
        ):
        sg[x,y] = grid[x,y] + sg[x,y-1] + sg[x-1,y] - sg[x-1,y-1]
    return sg

def high_spot_3(sumgrid):
    best_total = -100
    for (x,y) in itertools.product(
            range(1, sumgrid.width-2),
            range(1, sumgrid.height-2)
        ):
        total = sum_range(sumgrid, x, y, 3)
        if total > best_total:
            best_total = total
            best = (x,y)
    return best

def high_spot_any(sumgrid):
    best_total = -100
    for (x,y) in itertools.product(
            range(1, sumgrid.width),
            range(1, sumgrid.height)
        ):
        ms = 1 + min(sumgrid.width-x, sumgrid.height-y)
        for size in range(1, ms):
            total = sum_range(sumgrid, x, y, size)
            if total > best_total:
                best_total = total
                best = (x,y,size)
    return best

def sum_range(sg, x,y, size):
    x0 = x-1
    y0 = y-1
    x1 = x0+size
    y1 = y0+size
    return sg[x1,y1] + sg[x0,y0] - sg[x0,y1] - sg[x1,y0]

def main():
    serial = int(sys.argv[1])
    grid = make_grid(serial)
    sumgrid = make_sum_grid(grid)
    x,y = high_spot_3(sumgrid)
    print(f"High spot for 3 by 3: {x},{y}")
    print("with total:", sum_range(sumgrid, x, y, 3))
    x,y,size = high_spot_any(sumgrid)
    print(f"High spot for any size: {x},{y},{size}")
    print("with total:", sum_range(sumgrid, x, y, size))

if __name__ == '__main__':
    main()
