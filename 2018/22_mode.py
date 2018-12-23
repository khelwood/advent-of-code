#!/usr/bin/env python3

import sys
import re
import itertools
from collections import defaultdict

ROCKY = 0
WET = 1
NARROW = 2

TORCH = 1
GEAR = 2
NEITHER = 0

TOOL_TERRAIN = { TORCH: {ROCKY, NARROW}, GEAR: {ROCKY, WET},
                     NEITHER: {WET, NARROW} }
TERRAIN_TOOL = { ROCKY: {GEAR, TORCH}, WET: {GEAR, NEITHER},
                     NARROW: {TORCH, NEITHER} }
TOOL_TIME = 7
TRAVEL_TIME = 1

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
    def adjacent(self, x, y):
        tx,ty = self.target
        dx = tx-x
        dy = ty-y
        if abs(dx) > abs(dy):
            if dx > 0:
                yield (x+1,y)
                if dy > 0:
                    yield (x,y+1)
                    if y>0:
                        yield (x,y-1)
                else:
                    if y>0:
                        yield (x,y-1)
                    yield (x,y+1)
                if x>0:
                    yield (x-1,y)
            else:
                if x>0:
                    yield (x-1,y)
                if dy > 0:
                    yield (x,y+1)
                    if y>0:
                        yield (x,y-1)
                else:
                    if y>0:
                        yield (x,y-1)
                    yield (x,y+1)
                yield (x+1,y)
        else:
            if dy > 0:
                yield (x,y+1)
                if dx > 0:
                    yield (x+1,y)
                    if x>0:
                        yield (x-1,y)
                else:
                    if x>0:
                        yield (x-1,y)
                    yield (x+1,y)
                if y>0:
                    yield (x,y-1)
            else:
                if y>0:
                    yield (x,y-1)
                if dx > 0:
                    yield (x+1,y)
                    if x>0:
                        yield (x-1,y)
                else:
                    if x>0:
                        yield (x-1,y)
                    yield (x+1,y)
                yield (x,y+1)

    def moves(self, state, tterrains=TOOL_TERRAIN, ttools=TERRAIN_TOOL):
        x,y,tool = state
        terrains = tterrains[tool]
        fast = []
        slow = []
        ht = self[x,y]
        for pos in self.adjacent(x,y):
            sp = self[pos]
            if sp in terrains:
                fast.append(pos+(tool,))
            else:
                newtool = next(iter(ttools[sp]&ttools[ht]))
                slow.append(pos+(newtool,))
        return fast,slow

def simple_time(cave, tterrains=TOOL_TERRAIN):
    state = (0,0,TORCH)
    time = 0
    tx,ty = cave.target
    toolnames = "none torch gear".split()
    while state[:2] != cave.target:
        x,y,t = state
        terrains = tterrains[t]
        if y < ty and cave[x,y+1] in terrains:
            time += TRAVEL_TIME
            state = (x,y+1,t)
            continue
        if x < tx and cave[x+1,y] in terrains:
            time += TRAVEL_TIME
            state = (x+1,y,t)
            continue
        if abs(tx-x) > abs(ty-y):
            newtool = (tterrains[cave[x,y]] & tterrains[cave[x+1,y]])
            newtool = next(iter(newtools))
            time += TOOL_TIME + TRAVEL_TIME
            state = (x+1, y, newtool)
            continue
        newtool = (tterrains[cave[x,y]] & tterrains[cave[x,y+1]])
        newtool = next(iter(newtool))
        time += TOOL_TIME + TRAVEL_TIME
        state = (x, y+1, newtool)
    if state[-1] != TORCH:
        time += TRAVEL_TIME
    return time

def setmin(dct, key, value):
    dct[key] = min(value, dct.get(key, value))

def solve(cave, maxtime):
    state = (0,0,TORCH)
    dist_pos = defaultdict(set)
    dist_pos[0] = {state}
    seen = set()
    tx,ty = cave.target
    for time in range(maxtime):
        for state in dist_pos[time]:
            x,y,tool = state
            if state in seen:
                continue
            seen.add(state)
            if abs(x-tx) + abs(y-ty)==1:
                newtime = time + TRAVEL_TIME
                if tool!=TORCH:
                    newtime += TOOL_TIME
                if newtime < maxtime:
                    maxtime = newtime
                    dist_pos[newtime].add((tx,ty,TORCH))
                continue
            fast,slow = cave.moves(state)
            newtime = time + TRAVEL_TIME
            for m in fast:
                if m in seen:
                    continue
                nx,ny,ntool = m
                if newtime + abs(nx-tx) + abs(ny-ty) >= maxtime:
                    continue
                dist_pos[newtime].add(m)
            newtime += TOOL_TIME
            if newtime >= maxtime:
                continue
            for m in slow:
                if m in seen:
                    continue
                nx,ny,ntool = m
                if newtime + abs(nx-tx) + abs(ny-ty) >= maxtime:
                    continue
                dist_pos[newtime].add(m)
    return maxtime

def main():
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])
        target = tuple(map(int, sys.argv[2:4]))
    else:
        depth, target = read_input()
    cave = Cave(depth, target)
    #cave.display(10,10)
    tx,ty = target
    risk = sum(cave[p] for p in itertools.product(range(tx+1), range(ty+1)))
    print("Total risk:", risk)
    stime = simple_time(cave)
    print("Simple route time:", stime) # 2354 -- upper bound
    time = solve(cave, stime)
    print("Shortest time:", time)

if __name__ == '__main__':
    main()
