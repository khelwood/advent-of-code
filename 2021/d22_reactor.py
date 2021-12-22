#!/usr/bin/env python3

import sys
import re
from itertools import product
from typing import NamedTuple

class Cube(NamedTuple):
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    def __contains__(self, p):
        x,y,z = p
        return (self.x0 <= x <= self.x1
                and self.y0 <= y <= self.y1
                and self.z0 <= z <= self.z1)

    def __and__(self, other):
        return Cube(max(self.x0, other.x0),
                    min(self.x1, other.x1),
                    max(self.y0, other.y0),
                    min(self.y1, other.y1),
                    max(self.z0, other.z0),
                    min(self.z1, other.z1),
                )

    def __iter__(self):
        return product(range(self.x0, self.x1+1),
            range(self.y0, self.y1+1),
            range(self.z0, self.z1+1))

    def __bool__(self):
        return (self.x0 <= self.x1 and self.y0 <= self.y1
                and self.z0 <= self.z1)

    def volume(self):
        if not self:
            return 0
        return ((self.x1 + 1 - self.x0) * (self.y1 + 1 - self.y0)
                * (self.z1 + 1 - self.z0))

    @classmethod
    def parse(cls, line, ptn=re.compile(r'^(on|off) x=#..#,y=#..#,z=#..#$'
          .replace(' ',r'\s*').replace('.',r'\.').replace('#', r'(-?\d+)'))):
        m = ptn.match(line)
        on = m.group(1)=='on'
        return on, cls(*(int(m.group(i)) for i in range(2,8)))


class CubeCombo:
    def __init__(self, cube):
        self.cube = cube
        self.subs = []

    def volume(self):
        vol = self.cube.volume()
        for c in self.subs:
            vol -= c.volume()
        return vol

    def __isub__(self, other: Cube):
        x = other&self.cube
        if x:
            for c in self.subs:
                c -= x
            self.subs.append(CubeCombo(x))
        return self


def volume_on_in_cubes(cubes):
    ccs = []
    for on,cube in cubes:
        for cc in ccs:
            cc -= cube
        if on:
            ccs.append(CubeCombo(cube))
    return sum(cc.volume() for cc in ccs)


def main():
    cubes = tuple(Cube.parse(s) for s in sys.stdin.read().strip().splitlines())
    zone = Cube(*((-50,50)*3))
    onset = set()
    for on,cube in cubes:
        cube = cube & zone
        if on:
            onset.update(cube)
        else:
            onset.difference_update(cube)
    print("Initialisation:", len(onset))
    print("Main:", volume_on_in_cubes(cubes))

if __name__ == '__main__':
    main()
