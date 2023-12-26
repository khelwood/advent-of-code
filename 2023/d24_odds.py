#!/usr/bin/env python3

import sys
import re
import z3

from typing import NamedTuple
from itertools import combinations

HAIL_PTN = re.compile(' # , # , # @ # , # , # '
    .replace(' ',r'\s*').replace('#', r'(-?\d+)'))

class Hail:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

def intersect(a, b):
    """
    ax + s*ux = bx + t*vx
    ay + s*uy = by + t*vy

    s = (bx + t*vx - ax) / ux

    ay + s*uy = by + t*vy
    ay + (bx + t*vx - ax)*uy/ux = by + t*ux
    ay + bx*uy/ux + t*vx*uy/ux - ax*uy/ux = by + t*ux
    t*(vx*uy/ux - ux) = by - ay - bx*uy/ux + ax*uy/ux
    t = (by - ay - bx*uy/ux + ax*uy/ux) / (vx*uy/ux - ux)
    """

    if a.vel[0]==0:
        if b.vel[0]==0:
            return None
        a,b = b,a
    ax,ay = a.pos[:2]
    ux,uy = a.vel[:2]
    bx,by = b.pos[:2]
    vx,vy = b.vel[:2]
    if uy*vx==ux*vy:
        return None
    t = (by - ay - uy*bx/ux + uy*ax/ux) / (uy*vx/ux - vy)
    if t < 0:
        return None
    s = (bx + t*vx - ax) / ux
    if s < 0:
        return None
    x = bx + t*vx
    y = by + t*vy
    return (x,y)


def parse_hail(line):
    m = HAIL_PTN.fullmatch(line)
    if not m:
        raise ValueError(repr(line))
    nums = tuple(map(int, m.groups()))
    return Hail(nums[:3], nums[3:])

def count_intersections(hails, mindist, maxdist):
    """
    Line 1: a[1]x + b[1]y + c[1] = 0
    Line 2: a[2]x + b[2]y + c[2] = 0

    (x[0],y[0]) = (b[1]c[2]-b[2]c[1], c[1]a[2]-c[2]a[1]) all / (a[1]b[2] - a[2]b[1])
    """
    count = 0
    for a,b in combinations(hails, 2):
        p = intersect(a,b)
        if p is not None:
            x,y = p
            if mindist <= x <= maxdist and mindist <= y <= maxdist:
                count += 1
    return count

def find_throw_start(hails):
    sol = z3.Solver()
    x = z3.Int('x')
    y = z3.Int('y')
    z = z3.Int('z')
    vx = z3.Int('vx')
    vy = z3.Int('vy')
    vz = z3.Int('vz')
    for i,hail in enumerate(hails):
        hx,hy,hz = hail.pos
        ux,uy,uz = hail.vel
        tvar = z3.Int(f't{i}')
        sol.add(tvar >= 0)
        sol.add(x + tvar*vx == hx + tvar*ux)
        sol.add(y + tvar*vy == hy + tvar*uy)
        sol.add(z + tvar*vz == hz + tvar*uz)
    assert sol.check()==z3.sat
    model = sol.model()
    return tuple(model[coord].as_long() for coord in (x,y,z))


def main():
    hails = list(map(parse_hail, sys.stdin.read().strip().splitlines()))

    mindist = 200_000_000_000_000
    maxdist = 400_000_000_000_000
    if len(hails) < 100:
        mindist = 7
        maxdist = 27
    print("Part 1:", count_intersections(hails, mindist, maxdist))
    print("Part 2:", sum(find_throw_start(hails)))

if __name__ == '__main__':
    main()
