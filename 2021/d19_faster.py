#!/usr/bin/env python3

import sys

from itertools import combinations
from collections import defaultdict
from ast import literal_eval as leval

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def subp(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def dotp(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def negp(a):
    return (-a[0], -a[1], -a[2])


def setup_rotations():
    x = (1,0,0)
    y = (0,1,0)
    z = (0,0,1)
    _x = (-1,0,0)
    _y = (0,-1,0)
    _z = (0,0,-1)
    rots = [(x,y,z), (_x,z,y), (z,_y, x), (y,x,_z),
            (_x,_y, z), (x,_y,_z), (_x,y,_z), (_x,_z,_y)]
    return rots + [(b,c,a) for (a,b,c) in rots] + [(c,a,b) for (a,b,c) in rots]

class Rotation(tuple):
    def __call__(self, v):
        return tuple(dotp(a,v) for a in self)

ROTATIONS = tuple(map(Rotation, setup_rotations()))

class Scanner:
    def __init__(self):
        self.beacons = []
        self.fixed = False

    def fix(self, disp, rot):
        self.position = disp or (0,0,0)
        if disp is not None:
            self.beacons = [addp(disp, rot(p)) for p in self.beacons]
            self.symmetric_diffs = calculate_differences(self.beacons, True)
        self.beacon_set = set(self.beacons)
        self.true_diffs = calculate_differences(self.beacons, False)
        self.fixed = True

def calculate_differences(beacons, symmetric=False):
    diffs = defaultdict(set)
    for a,b in combinations(beacons, 2):
        d = subp(b,a)
        if symmetric:
            d = tuple(sorted(map(abs, d)))
            diffs[a].add(d)
            diffs[b].add(d)
        else:
            diffs[a].add(d)
            diffs[b].add(negp(d))
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
            sc.beacons.append(leval(line))
        elif 'scanner' in line:
            sc = Scanner()
            scanners.append(sc)
    return scanners

def find_rotation(a, b, p1, p2):
    adiffs = a.true_diffs[p1]
    for rot in ROTATIONS:
        bp = rot(p2)
        bdiffs = {subp(rot(p),bp) for p in b.beacons}
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
            disp = subp(p1, rotp)
            b.fix(disp, rot)
            fixed.append(b)
        unfixed = [sc for sc in unfixed if not sc.fixed]
    assert not unfixed

    all_beacons = set.union(*(sc.beacon_set for sc in scanners))
    print("Number of beacons:", len(all_beacons))

    max_manhattan = max(sum(map(abs, subp(a.position,b.position)))
                        for (a,b) in combinations(scanners, 2))
    print("Max distance:", max_manhattan)


if __name__ == '__main__':
    main()
