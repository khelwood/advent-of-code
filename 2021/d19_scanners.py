#!/usr/bin/env python3

import sys
import re
import itertools
from ast import literal_eval as leval

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def subp(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

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

    def __repr__(self):
        return f'scanner {self.index}'


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

def main():
    scanners = read_scanners()
    for sc in scanners:
        sc.calculate_differences()
        sc.fixed = False
    scanners[0].fixed = True
    fixed = [scanners[0]]
    unfixed = scanners[1:]
    for a in fixed:
        new_fixed = []
        for b in unfixed:
            p1,p2 = a.compare_differences(b)
            if p1 is None:
                continue
            print(f'{p1} in {a} is {p2} in {b}')
            # fix b
            b.fixed = True
            fixed.append(b)
        unfixed = [sc for sc in unfixed if not sc.fixed]


if __name__ == '__main__':
    main()
