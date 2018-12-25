#!/usr/bin/env python3

import sys
from itertools import combinations

def read_point(line):
    return tuple(map(int, line.replace(',',' ').split()))

def manhattan(a, b):
    return (abs(a[0]-b[0]) + abs(a[1]-b[1])
                + abs(a[2]-b[2]) + abs(a[3]-b[3]))

def count_constellations(points):
    constellations = { p: {p} for p in points }
    for a,b in combinations(points,2):
        ca = constellations[a]
        cb = constellations[b]
        if ca is not cb and manhattan(a,b) <= 3:
            ca.update(cb)
            for p in cb:
                constellations[p] = ca
    return len(set(map(id, constellations.values())))

def main():
    points = [read_point(ln) for ln in sys.stdin.read().strip().splitlines()]
    print("Num constellations:", count_constellations(points))

if __name__ == '__main__':
    main()
