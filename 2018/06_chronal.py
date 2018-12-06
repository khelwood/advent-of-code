#!/usr/bin/env python3

import sys

def psub(p,q):
    return (p[0]-q[0], p[1]-q[1])

def padd(p,q):
    return (p[0]+q[0], p[1]+q[1])

class BoundedGrid:
    def __init__(self, p0, p1):
        w,h = psub(p1,p0)
        self._data = [['.']*w for _ in range(h)]
        self._min = p0
    width = property(lambda self: len(self._data[0]))
    height = property(lambda self: len(self._data))
    min = property(lambda self: self._min)
    def __getitem__(self, p):
        x,y = psub(p, self.min)
        return self._data[y][x]
    def __setitem__(self, p, value):
        x,y = psub(p, self.min)
        self._data[y][x] = value
    def coords(self):
        x0,y0 = self.min
        xran = range(x0, x0+self.width)
        for y in range(y0, y0+self.height):
            for x in xran:
                yield (x,y)
    def values(self):
        for row in self._data:
            yield from row
    def display(self):
        for row in self._data:
            print(''.join([str(x).center(3) for x in row]))

def manhattan(p,q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

def bounds(coords):
    (x0,y0) = (x1,y1) = coords[0]
    for (x,y) in coords:
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)
    return (x0,y0), (x1,y1)

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

def main():
    coords = [tuple(int(x.strip()) for x in line.split(','))
                  for line in sys.stdin.read().splitlines()]
    p0, p1 = bounds(coords)
    grid = BoundedGrid(psub(p0, (1,1)), padd(p1, (2,2)))
    for p in grid.coords():
        grid[p] = closest(coords, p)
    infinite = set()
    x0, y0 = grid.min
    for y in (y0, y0+grid.height-1):
        for x in range(x0, x0+grid.width):
            infinite.add(grid[x,y])
    for x in (x0, x0+grid.width-1):
        for y in range(y0, y0+grid.height):
            infinite.add(grid[x,y])
    areas = [0]*len(coords)
    for value in grid.values():
        if value not in infinite:
            areas[value] += 1
    biggest = max(areas)
    print("Biggest area:", biggest)
    LIMIT = 10_000
    goodcount = sum(sum(manhattan(p,c) for c in coords) < LIMIT
                        for p in grid.coords())
    print("Size of good region:", goodcount)
    
        

if __name__ == '__main__':
    main()
