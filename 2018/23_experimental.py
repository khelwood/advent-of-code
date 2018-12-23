#!/usr/bin/env python3

import sys
import re
from collections import namedtuple, defaultdict

Nanobot = namedtuple('Nanobot', 'x y z radius')
Nanobot.pos = property(lambda bot: bot[:3])
Nanobot.inrange = lambda self, pos: (manhattan(self, pos) <= self.radius)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def read_bot(line):
    line = line.strip()
    m = re.match('pos = < # , # , # > , r = # $'
                     .replace(' ',r'\s*').replace('#', r'(-?\d+)'), line)
    if not m:
        raise ValueError(repr(line))
    return Nanobot(*map(int, m.groups()))

def sign(v):
    return (1 if v>0 else -1 if v<0 else 0)

class BotZone:
    __slots__ = ('bots', 'cache', 'sx', 'sy', 'sz')
    def __init__(self, bots, start):
        self.bots = tuple(sorted(bots, key=lambda bot: bot.radius))
        self.sx, self.sy, self.sz = map(sign, start)
        self.cache = {}
    def __getitem__(self, pos):
        cache = self.cache
        v = cache.get(pos)
        if v is None:
            x,y,z = pos
            if (x < 0 and self.sx >= 0 or
                    x > 0 and self.sy <= 0 or
                    y < 0 and self.sy >= 0 or
                    y > 0 and self.sy <= 0 or
                    z > 0 and self.sz <=0 or
                    z < 0 and self.sz >= 0):
                cache[pos] = v = False
            else:
                cache[pos] = v = all(bot.inrange(pos) for bot in self.bots)
        return v

def all_corners(bots):
    for bot in bots:
        x,y,z,r = bot
        yield (x+r,y,z)
        yield (x-r,y,z)
        yield (x,y+r,z)
        yield (x,y-r,z)
        yield (x,y,z+r)
        yield (x,y,z-r)

def find_v(pos, zone):
    x,y,z = pos
    vx=vy=vz=0
    dx,dy,dz = (1 if v < 0 else -1 for v in pos)
    if x!=0 and zone[x+dx,y,z]:
        vx = dx
    if y!=0 and zone[x,y+dy,z]:
        vy = dy
    if z!=0 and zone[x,y,z+dz]:
        vz = dz
    return (vx,vy,vz)

def directions(vx,vy,vz):
    if vx and vy and vz:
        yield (vx,vy,vz)
    if vx and vy:
        yield (vx,vy,0)
    if vx and vz:
        yield (vx,0,vz)
    if vy and vz:
        yield (0,vy,vz)
    if vx:
        yield (vx,0,0)
    if vy:
        yield (0,vy,0)
    if vz:
        yield (0,0,vz)

def fast_directions(vx,vy,vz, scale):
    for dx,dy,dz in directions(vx,vy,vz):
        yield (dx*scale, dy*scale, dz*scale)

def addp(a,b):
  return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def bring_in(pos, zone):
    try:
        while True:
            old = pos
            v = find_v(pos, zone)
            scale = 1_000_000
            while scale:
                for d in fast_directions(*v, scale):
                    n = addp(pos, d)
                    if zone[n]:
                        pos = n
                        n = addp(pos, d)
                        break
                if pos != old:
                    break
                scale //= 100
            if pos==old:
                break
        return pos
    except:
        print("\npos:",pos)
        raise

def main():
    bots = [read_bot(line) for line in sys.stdin.read().strip().splitlines()]
    strongest = max(bots, key=lambda bot: bot.radius)
    inrange = sum(strongest.inrange(bot) for bot in bots)
    print("In range:", inrange)
    corners = set(all_corners(bots))
    best_count = 0
    for corner in corners:
        count = sum(bot.inrange(corner) for bot in bots)
        if count < best_count:
            continue
        if count > best_count:
            best_count = count
            best = []
        best.append(corner)
    print("Best count:", best_count)
    print("Best corners:", best)
    best = next(iter(best))
    nearby = BotZone((bot for bot in bots if bot.inrange(best)), best)
    nearest = bring_in(best, nearby)
    print("Nearest:", nearest)
    print("Distance from origin:", sum(map(abs, nearest)))

if __name__ == '__main__':
    main()
