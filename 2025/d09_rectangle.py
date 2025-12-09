#!/usr/bin/env python3

import sys
from itertools import combinations, product

RED = 1
GREEN = 2

def sign(d):
    return (1 if d>=0 else -1)

def read_input():
    lines = filter(bool, map(str.strip, sys.stdin))
    return [tuple(map(int, s.split(','))) for s in lines]

def rect_area(a,b):
    ax,ay = a
    bx,by = b
    return (abs(ax-bx)+1)*(abs(ay-by)+1)

def iter_line(a,b):
    ax,ay = a
    bx,by = b
    if ax==bx:
        d = sign(by-ay)
        return ((ax,y) for y in range(ay+d, by, d))
    if ay==by:
        d = sign(bx-ax)
        return ((x,ay) for x in range(ax+d, bx, d))
    raise ValueError(f"Mismatched points: {a}, {b}")

def make_grid(reds):
    grid = {r:RED for r in reds}
    last = reds[-1]
    for r in reds:
        for g in iter_line(last, r):
            grid[g] = GREEN
        last = r
    return grid

def find_inner_point(grid):
    x,y = min(grid)
    return (x+1, y+1)

def flood_fill(grid, p, fill):
    ps = [p]
    for p in ps:
        ol = len(grid)
        if p in grid:
            continue
        x,y = p
        x0 = x
        while (x0-1,y) not in grid:
            x0 -= 1
        x1 = x+1
        while (x1,y) not in grid:
            if x1 > 98273:
                raise ValueError(f"run off side of shape at {p}")
            x1 += 1
        for x in range(x0,x1):
            p = x,y
            if p in grid:
                continue
            grid[p] = fill
            p = (x, y-1)
            if p not in grid:
                ps.append(p)
            p = (x, y+1)
            if p not in grid:
                ps.append(p)
        nl = len(grid)
        if nl > ol and nl//1_000_000 != ol//1_000_000:
            print(nl)

def draw_grid(grid):
    xmax = max(x for (x,y) in grid)
    ymax = max(y for (x,y) in grid)
    for y in range(0, ymax+1):
        for x in range(0, xmax+1):
            v = grid.get((x,y))
            if v==RED:
                ch = '#'
            elif v==GREEN:
                ch = 'X'
            else:
                ch = '.'
            print(ch, end='')
        print()

def check_colour(grid, a, b):
    ax,ay = a
    bx,by = b
    x0 = min(ax,bx)
    y0 = min(ay,by)
    x1 = max(ax,bx)+1
    y1 = max(ay,by)+1
    return all(p in grid for p in product(range(x0,x1), range(y0,y1)))


def find_max_colour_rect(grid, reds):
    best = 0
    for a,b in combinations(reds, 2):
        ra = rect_area(a,b)
        if ra > best and check_colour(grid, a, b):
            best = ra
    return best

def main():
    reds = read_input()
    print(max(rect_area(a,b) for (a,b) in combinations(reds, 2)))
    grid = make_grid(reds)
    if len(reds) < 100:
        p = find_inner_point(reds)
        assert p not in grid
        flood_fill(grid, p, GREEN)
        draw_grid(grid)
        print(find_max_colour_rect(grid,reds))


if __name__ == '__main__':
    main()
