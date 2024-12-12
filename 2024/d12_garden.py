#!/usr/bin/env python3

import sys

class Garden:
    def __init__(self, lines):
        self.lines = lines
    def __getitem__(self, p):
        if p not in self:
            return None
        x,y = p
        return self.lines[y][x]
    @property
    def width(self):
        return len(self.lines[0])
    @property
    def height(self):
        return len(self.lines)
    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.width and 0 <= y < self.height)
    def __iter__(self):
        xr = range(self.width)
        return ((x,y) for y in range(self.height) for x in xr)


def read_garden():
    return Garden(sys.stdin.read().strip().splitlines())

def find_regions(garden):
    regions = []
    cells_done = set()
    for p in garden:
        if p not in cells_done:
            region = find_region(garden, p)
            regions.append(region)
            cells_done.update(region)
    return regions

def find_region(garden, p):
    """Flood fill from point p, using a set to mark the filled points."""
    region = set()
    v = garden[p]
    stack = [p]
    wid = garden.width
    hei = garden.height
    while stack:
        p = stack.pop()
        if p in region or garden[p]!=v:
            continue
        x,y = p
        ran1 = range(x,wid)
        ran2 = range(x-1, -1, -1)
        for ran in (ran1, ran2):
            for xi in ran:
                p = (xi,y)
                if garden[p] != v or p in region:
                    break
                region.add(p)
                if y > 0:
                    q = (xi,y-1)
                    if q not in region and garden[q]==v:
                        stack.append(q)
                if y < hei-1:
                    q = (xi,y+1)
                    if q not in region and garden[q]==v:
                        stack.append(q)
    return region


def neighbours(p):
    x,y = p
    yield (x-1,y)
    yield (x,y-1)
    yield (x+1,y)
    yield (x,y+1)

def perimeter(region):
    c = 0
    for p in region:
        for n in neighbours(p):
            if n not in region:
                c += 1
    return c

DIRECTIONS = tuple(neighbours((0,0)))

def find_sides(region):
    sides = []
    done = set()
    for p in region:
        for d in DIRECTIONS:
            if (p,d) in done:
                continue
            n = (p[0]+d[0], p[1]+d[1])
            if n in region:
                continue
            side = scan_side(region, p, d)
            sides.append(sides)
            for s in side:
                done.add((s,d))
    return sides

def scan_side(region, p, d):
    side = set()
    x,y = p
    dx,dy = d
    if dx==0:
        xi = x
        while (xi,y) in region and (xi,y+dy) not in region:
            side.add((xi,y))
            xi += 1
        xi = x-1
        while (xi,y) in region and (xi,y+dy) not in region:
            side.add((xi,y))
            xi -= 1
    else:
        yi = y
        while (x,yi) in region and (x+dx,yi) not in region:
            side.add((x,yi))
            yi += 1
        yi = y-1
        while (x,yi) in region and (x+dx,yi) not in region:
            side.add((x,yi))
            yi -= 1
    return side

def main():
    garden = read_garden()
    regions = find_regions(garden)
    cost1 = sum(len(region)*perimeter(region) for region in regions)
    print(cost1)
    cost2 = sum(len(region)*len(find_sides(region)) for region in regions)
    print(cost2)


if __name__ == '__main__':
    main()
