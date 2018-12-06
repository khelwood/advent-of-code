#!/usr/bin/env python3

import sys
sys.path.append('..')
from grid import Grid

def manhattan(p,q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

def closest(coords, pos):
    best = -1
    dist = None
    for i,c in enumerate(coords):
        d = manhattan(pos,c)
        if dist is None or d < dist:
            dist = d
            best = i
        elif d==dist:
            best = -1
    return best

def normalise(coords):
    (x0,y0) = (x1,y1) = coords[0]
    for (x,y) in coords:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    coords[:] = [(x-x0, y-y0) for (x,y) in coords]
    return x1-x0, y1-y0

def main():
    coords = [tuple(int(x.strip()) for x in line.split(','))
                  for line in sys.stdin.read().splitlines()]
    w,h = normalise(coords)
    grid = Grid(w,h)
    for p in grid:
        grid[p] = closest(coords, p)
    infinite = set()
    for y in (0, grid.height-1):
        for x in range(grid.width):
            infinite.add(grid[x,y])
    for x in (0, grid.width-1):
        for y in range(1, grid.height-1):
            infinite.add(grid[x,y])
    areas = [0]*len(coords)
    for value in grid.values():
        if value not in infinite:
            areas[value] += 1
    biggest = max(areas)
    print("Biggest area:", biggest)
    LIMIT = 10_000
    goodcount = sum(sum(manhattan(p,c) for c in coords) < LIMIT
                        for p in grid)
    print("Size of good region:", goodcount)
    
        

if __name__ == '__main__':
    main()
