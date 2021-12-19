#!/usr/bin/env python3

import sys
import re
import itertools
from ast import literal_eval as leval

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def subp(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def setup_rotations():
    x = (1,0,0)
    y = (0,1,0)
    z = (0,0,1)
    _x = (-1,0,0)
    _y = (0,-1,0)
    _z = (0,0,-1)
    rots = [(x,y,z), (_x,z,y), (z,_y, x), (y,x,_z),
            (_x,_y, z), (x,_y,_z), (_x,y,_z),
            (_x,_z,_y)]
    return rots + [(b,c,a) for (a,b,c) in rots] + [(c,a,b) for (a,b,c) in rots]

class Rotation:
    __slots__ = ('matrix',)
    def __init__(self, matrix):
        self.matrix = matrix
    def __repr__(self):
        return f'Rotation{self.matrix}'
    def __str__(self):
        return 'Rotation:\n' + '\n'.join(map(str, self.matrix))
    def __call__(self, v):
        m = self.matrix
        return tuple(dot(a,v) for a in self.matrix)

ROTATIONS = tuple(map(Rotation, setup_rotations()))

def sort3(a,b,c):
    if a <= b:
        if a <= c:
            if b <= c:
                return (a,b,c)
            return (a,c,b)
        return (c,a,b)
    if b <= c:
        if c <= a:
            return (b, c, a)
        return (b, a, c)
    return (c,b,a)

class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = []
        self.fixed = False

    def calculate_differences(self):
        diffs = {}
        for a in self.beacons:
            adiffs = set()
            for b in self.beacons:
                if a is not b:
                    dx,dy,dz = subp(a,b)
                    dx = abs(dx)
                    dy = abs(dy)
                    dz = abs(dz)
                    adiffs.add(sort3(dx,dy,dz))
            diffs[a] = adiffs
        self.diffs = diffs

    def compare_differences(self, other):
        for p1,d1 in self.diffs.items():
            for p2,d2 in other.diffs.items():
                if len(d1&d2) >= 11:
                    return (p1,p2)
        return None,None

    def fix(self, disp, rot):
        if disp is not None:
            self.beacons = [addp(disp, rot(p)) for p in self.beacons]
        self.beacon_set = set(self.beacons)
        self.fixed_diffs = calculate_fixed_diffs(self.beacons)
        if disp is not None:
            self.calculate_differences()
        self.fixed = True

    def __repr__(self):
        return f'scanner {self.index}'


def calculate_fixed_diffs(beacons):
    fixed_diffs = {}
    for a in beacons:
        adiffs = set()
        for b in beacons:
            if a is b:
                continue
            adiffs.add(subp(b,a))
        fixed_diffs[a] = adiffs
    return fixed_diffs

def read_scanners():
    scanners = []
    ptn = re.compile(r'--- scanner (\d+) ---')
    for line in sys.stdin.read().strip().splitlines():
        if ',' in line:
            sc.beacons.append(leval(line))
        else:
            m = re.match(ptn, line)
            if m:
                sc = Scanner(int(m.group(1)))
                scanners.append(sc)
    return scanners

def find_rotation(a, b, p1, p2):
    adiffs = a.fixed_diffs[p1]
    for r in ROTATIONS:
        bp = r(p2)
        bpoints = [r(p) for p in b.beacons]
        bdiffs = {subp(p,bp) for p in bpoints if p!=bp}
        if len(bdiffs&adiffs) >= 11:
            return r
    return None

def main():
    scanners = read_scanners()
    for sc in scanners:
        sc.calculate_differences()
    sc = scanners[0]
    sc.fix(None, None)

    fixed = [scanners[0]]
    unfixed = scanners[1:]
    for a in fixed:
        new_fixed = []
        for b in unfixed:
            p1,p2 = a.compare_differences(b)
            if p1 is None:
                continue
            print(f'{p1} in {a} is {p2} in {b}')
            rot = find_rotation(a, b, p1, p2)
            if rot is None:
                print("(no rotation found)")
                continue
            print(rot)
            rotp = rot(p2)
            disp = subp(p1, rotp)
            b.fix(disp, rot)
            fixed.append(b)
        unfixed = [sc for sc in unfixed if not sc.fixed]
    all_beacons = set.union(*(sc.beacon_set for sc in scanners))
    #print('\n'.join(map(str, sorted(all_beacons))))
    # 882: TOO HIGH
    print("Number of beacons:", len(all_beacons))


if __name__ == '__main__':
    main()
