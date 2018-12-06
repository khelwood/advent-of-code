#!/usr/bin/env python3

import sys
import itertools

def bounds(coords):
    (x0,y0) = (x1,y1) = coords[0]
    for (x,y) in coords:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return x0,y0,x1+1,y1+1

def make_regions(dists, x0,y0, x1,y1):
    regions = {}
    for pos in itertools.product(range(x0,x1), range(y0,y1)):
        region = None
        dist = x1 + y1 - x0 - y0
        for i,d in enumerate(dists[pos]):
            if d < dist:
                region = i
                dist = d
            elif d==dist:
                region = -1
        regions[pos] = region
    return regions

def main():
    coords = [tuple(int(x.strip()) for x in line.split(','))
                  for line in sys.stdin.read().splitlines()]
    x0,y0,x1,y1 = bounds(coords)
    dists = { (x,y): [abs(x-xi)+abs(y-yi) for (xi,yi) in coords]
              for x,y in itertools.product(range(x0,x1), range(y0,y1)) }
    regions = make_regions(dists, x0, y0, x1, y1)
    infinite = set()
    for p in itertools.product(range(x0,x1), (y0, y1-1)):
        infinite.add(regions[p])
    for p in itertools.product((x0,x1-1), range(y0+1, y1-1)):
        infinite.add(regions[p])
    areas = [0]*len(coords)
    for reg in regions.values():
        if reg not in infinite:
            areas[reg] += 1
    biggest = max(areas)
    print("Biggest area:", biggest)
    LIMIT = 10_000
    goodcount = sum(sum(v) < LIMIT for v in dists.values())
    print("Size of good region:", goodcount)

if __name__ == '__main__':
    main()
