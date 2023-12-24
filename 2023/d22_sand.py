#!/usr/bin/env python3

import sys
import re

from itertools import product
from typing import NamedTuple

INPUT_PTN = re.compile(r'#,#,#~#,#,#'.replace('#',r'(\d+)'))

class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self[0]+other[0], self[1]+other[1], self[2]+other[2])

    def __sub__(self, other):
        return Point(self[0]-other[0], self[1]-other[1], self[2]-other[2])

    @property
    def xy(self):
        return self[:2]

class Brick:
    def __init__(self, name, pos, vol):
        self.name = name
        self.pos = pos
        self.vol = vol

    @property
    def bottom(self):
        return self.pos.z

    def base(self):
        x,y,z = self.pos
        vx,vy,_ = self.vol
        for dx in range(vx):
            for dy in range(vy):
                yield Point(x+dx, y+dy, z)

    def surface(self):
        x,y,z = self.pos
        vx,vy,vz = self.vol
        for dx in range(vx):
            for dy in range(vy):
                yield Point(x+dx, y+dy, z+vz)

    def contents(self):
        x,y,z = self.pos
        vx,vy,vz = self.vol
        for dx in range(vx):
            for dy in range(vy):
                for dz in range(vz):
                    yield Point(x+dx, y+dy, z+dz)


def parse_brick(line, name):
    m = INPUT_PTN.fullmatch(line)
    if not m:
        raise ValueError(repr(line))
    nums = list(map(int, m.groups()))
    a = Point(*nums[:3])
    b = Point(*nums[3:])
    vol_offs = Point(1,1,1)
    if b < a:
        a,b = b,a
    return Brick(name, a, b + vol_offs - a)

def fall(brick, bricks, toplocs):
    height = 0
    btm = brick.bottom
    for p in brick.base():
        height = max(toplocs.get(p.xy, 1), height)
    if btm > height:
        brick.pos -= Point(0,0, btm-height)
    for p in brick.surface():
        xy = p.xy
        toplocs[xy] = max(toplocs.get(xy, 0), p.z)

def voxelise(bricks):
    voxels = {}
    for brick in bricks:
        for p in brick.contents():
            voxels[p] = brick
    return voxels

def find_all_supports(bricks, voxels):
    supports = {}
    down = Point(0,0,-1)
    for brick in bricks:
        supports[brick] = sups = set()
        for p in brick.base():
            other = voxels.get(p+down)
            if other:
                sups.add(other)
    return supports

def find_disposable(bricks, supports):
    needed = set()
    for brick in bricks:
        sups = supports[brick]
        if len(sups)==1:
            sup, = sups
            needed.add(sup)
    return set(bricks) - needed

def bounds(points):
    it = iter(points)
    p = next(it)
    x0,y0,z0 = p
    x1,y1,z1 = p
    for (x,y,z) in it:
        x0 = min(x0,x)
        y0 = min(y0,y)
        z0 = min(z0,z)
        x1 = max(x1,x)
        y1 = max(y1,y)
        z1 = max(z1,z)
    return (Point(x0,y0,z0), Point(x1,y1,z1))

def project(bricks, voxels):
    if voxels is None:
        voxels = voxelise(bricks)
    minp, maxp = bounds(voxels)
    for z in range(maxp.z, -1,-1):
        print(z, end=':  ')
        for x in range(minp.x, maxp.x+1):
            for y in range(minp.y, maxp.y+1):
                b = voxels.get((x,y,z))
                if b:
                    print(b.name, end='')
                    break
            else:
                print('-' if z==0 else '.', end='')
        print()

def chain_drop(brick, bricks, supports):
    dropped = {brick}
    for brick in bricks:
        if brick in dropped:
            continue
        sups = supports[brick]
        if sups and sups <= dropped:
            dropped.add(brick)
    return len(dropped) - 1

def main():
    oa = ord('A')
    lines = sys.stdin.read().strip().splitlines()
    bricks = [parse_brick(line, chr(oa+i)) for i,line in enumerate(lines)]
    bricks.sort(key=lambda b: (b.pos.z, b.pos))
    toplocs = {}
    for brick in bricks:
        fall(brick, bricks, toplocs)
    voxels = voxelise(bricks)
    supports = find_all_supports(bricks, voxels)
    dispo = find_disposable(bricks, supports)
    print("Part 1:", len(dispo))
    bricks.sort(key=lambda b: (b.pos.z, b.pos))
    total = sum(chain_drop(brick, bricks, supports) for brick in bricks)
    print("Part 2:", total)

if __name__ == '__main__':
    main()
