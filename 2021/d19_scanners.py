#!/usr/bin/env python3

import sys

from itertools import combinations
from typing import NamedTuple
from collections import defaultdict
from ast import literal_eval as leval

class Point(NamedTuple):
    x:int
    y:int
    z:int

    def __add__(self, other):
        return Point(self[0]+other[0], self[1]+other[1], self[2]+other[2])
    def __sub__(self, other):
        return Point(self[0]-other[0], self[1]-other[1], self[2]-other[2])
    def __neg__(self):
        return Point(-self[0], -self[1], -self[2])
    def __mul__(self, other):
        return self[0]*other[0] + self[1]*other[1] + self[2]*other[2]
    def abs(self):
        return Point(abs(self[0]), abs(self[1]), abs(self[2]))
    def d1(self):
        return sum(self.abs())

def setup_rotations():
    x = Point(1,0,0)
    y = Point(0,1,0)
    z = Point(0,0,1)
    rots = [(x,y,z), (-x,z,y), (z,-y, x), (y,x,-z),
            (-x,-y, z), (x,-y,-z), (-x,y,-z), (-x,-z,-y)]
    return rots + [(b,c,a) for (a,b,c) in rots] + [(c,a,b) for (a,b,c) in rots]

class Rotation(tuple):
    def __call__(self, v):
        return Point(*(a*v for a in self))

ROTATIONS = tuple(map(Rotation, setup_rotations()))

class Scanner:
    def __init__(self):
        self.beacons = []
        self.fixed = False

    def fix(self, disp, rot):
        self.position = disp or Point(0,0,0)
        if disp is not None:
            self.beacons = [disp + rot(p) for p in self.beacons]
            self.symmetric_diffs = calculate_differences(self.beacons, True)
        self.beacon_set = set(self.beacons)
        self.true_diffs = calculate_differences(self.beacons, False)
        self.fixed = True

def calculate_differences(beacons, symmetric=False):
    diffs = defaultdict(set)
    for a,b in combinations(beacons, 2):
        d = b-a
        if symmetric:
            d = Point(*sorted(d.abs()))
            diffs[a].add(d)
            diffs[b].add(d)
        else:
            diffs[a].add(d)
            diffs[b].add(-d)
    diffs.default_factory = None
    return diffs

def compare_differences(adiffs, bdiffs):
    for p1,d1 in adiffs.items():
        for p2,d2 in bdiffs.items():
            if len(d1&d2) >= 11:
                return (p1,p2)
    return (None,None)

def read_scanners():
    scanners = []
    for line in sys.stdin.read().strip().splitlines():
        if ',' in line:
            sc.beacons.append(Point(*leval(line)))
        elif 'scanner' in line:
            sc = Scanner()
            scanners.append(sc)
    return scanners

def find_rotation(a, b, p1, p2):
    adiffs = a.true_diffs[p1]
    for rot in ROTATIONS:
        bp = rot(p2)
        bdiffs = {rot(p)-bp for p in b.beacons}
        if len(bdiffs&adiffs) >= 11:
            return rot
    return None

def main():
    scanners = read_scanners()
    for sc in scanners:
        sc.symmetric_diffs = calculate_differences(sc.beacons, True)
    sc = scanners[0]
    sc.fix(None, None)

    fixed = [scanners[0]]
    unfixed = scanners[1:]
    for a in fixed:
        new_fixed = []
        for b in unfixed:
            p1,p2 = compare_differences(a.symmetric_diffs, b.symmetric_diffs)
            if p1 is None:
                continue
            rot = find_rotation(a, b, p1, p2)
            if rot is None:
                continue
            rotp = rot(p2)
            disp = p1 - rotp
            b.fix(disp, rot)
            fixed.append(b)
        unfixed = [sc for sc in unfixed if not sc.fixed]
    assert not unfixed

    all_beacons = set.union(*(sc.beacon_set for sc in scanners))
    print("Number of beacons:", len(all_beacons))

    max_manhattan = max((a.position-b.position).d1()
                        for (a,b) in combinations(scanners, 2))
    print("Max distance:", max_manhattan)


if __name__ == '__main__':
    main()
