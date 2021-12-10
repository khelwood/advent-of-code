#!/usr/bin/env python3

import sys
import math
from collections import Counter

DIRECTIONS = ((1,0), (0,1), (-1,0), (0,-1))

def addp(a, b):
    return (a[0]+b[0], a[1]+b[1])

def read_grid():
    grid = {}
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            grid[x,y] = int(ch)
    return grid,x+1,y+1

def neighbour_heights(grid, p, dirs=DIRECTIONS):
    for d in dirs:
        r = addp(p, d)
        h = grid.get(r)
        if h is not None:
            yield h

def find_low_points(grid):
    for p,h in grid.items():
        if all(h < nh for nh in neighbour_heights(grid, p)):
            yield p

def flood_fill(g, p, fill, wid, hei):
    stack = [p]
    while stack:
        p = stack.pop()
        if p in g:
            continue
        px,py = p
        for ran in (range(px, -1, -1), range(px+1, wid)):
            for x in ran:
                if (x,py) in g:
                    break
                g[x,py] = fill
                if py > 0 and (x,py-1) not in g:
                    stack.append((x,py-1))
                if py < hei-1 and (x,py+1) not in g:
                    stack.append((x,py+1))

def flood_fill_zones(grid, wid, hei, low_points):
    walls = [p for (p,h) in grid.items() if h==9]
    zones = {p:'W' for p in walls}
    for zone,p in enumerate(low_points):
        flood_fill(zones, p, zone, wid, hei)
    for p in walls:
        del zones[p]
    return zones

def main():
    grid,wid,hei = read_grid()
    low_points = list(find_low_points(grid))
    risk_sum = sum(grid[p]+1 for p in low_points)
    print("Risk sum:", risk_sum)
    zones = flood_fill_zones(grid,wid,hei,low_points)
    c = Counter(zones.values())
    basin_product = math.prod(v for (_,v) in c.most_common(3))
    print("Basin product:", basin_product)

if __name__ == '__main__':
    main()
