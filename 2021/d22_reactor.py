#!/usr/bin/env python3

import sys
import re
from itertools import product
from typing import NamedTuple

class Cube(NamedTuple):
    on: bool
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
        return Cube(self.on if self.on is not None else other.on,
                    max(self.x0, other.x0),
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


def read_cube(line,
        ptn=re.compile(r'^(on|off) x=#..#,y=#..#,z=#..#$'
          .replace(' ',r'\s*').replace('.',r'\.').replace('#', r'(-?\d+)'))
    ):
    m = ptn.match(line)
    on = m.group(1)=='on'
    ints = [int(m.group(i)) for i in range(2,8)]
    return Cube(on, *ints)


def main():
    cubes = tuple(read_cube(s) for s in sys.stdin.read().strip().splitlines())
    zone = Cube(None, *((-50,50)*3))
    on = set()
    for cube in cubes:
        cube = cube & zone
        if cube.on:
            on.update(cube)
        else:
            on.difference_update(cube)
    print("Number left on:", len(on))

if __name__ == '__main__':
    main()
