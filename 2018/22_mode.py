#!/usr/bin/env python3

import sys
import re
import itertools

ROCKY = 0
WET = 1
NARROW = 2

def read_input():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        m = re.match(r'depth:\s*(\d+)$', line)
        if m:
            depth = int(m.group(1))
            continue
        m = re.match(r'target:\s*(\d+)\s*,\s*(\d+)$', line)
        if m:
            target = tuple(map(int, m.groups()))
            continue
        raise ValueError(line)
    return depth, target

class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.geo_cache = { (0,0): 0, target: 0 }
        self.erosion_cache = {}
    def geo_index(self, p):
        v = self.geo_cache.get(p)
        if v is None:
            self.geo_cache[p] = v = self.calculate_geo(p)
        return v
    def calculate_geo(self, p):
        x,y = p
        if x==0:
            return y*48271
        if y==0:
            return x*16807
        return self.erosion_level((x-1,y)) * self.erosion_level((x,y-1))
    def erosion_level(self, p):
        v = self.erosion_cache.get(p)
        if v is None:
            self.erosion_cache[p] = v = self.calculate_erosion(p)
        return v
    def calculate_erosion(self, p):
        return (self.geo_index(p) + self.depth)%20183
    def __getitem__(self, p):
        return self.erosion_level(p) % 3
    def char(self, p, chars='.=|'):
        if p==(0,0):
            return 'M'
        if p==self.target:
            return 'T'
        return chars[self[p]]
    def display(self, w, h):
        xran = range(0,w)
        for y in range(0, h):
            print(''.join(self.char((x,y)) for x in xran))

def main():
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])
        target = tuple(map(int, sys.argv[2:4]))
    else:
        depth, target = read_input()
    cave = Cave(depth, target)
    tx,ty = target
    risk = sum(cave[p] for p in itertools.product(range(tx+1), range(ty+1)))
    print("Total risk:", risk)

if __name__ == '__main__':
    main()
