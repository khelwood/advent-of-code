#!/usr/bin/env python3

import sys
from itertools import combinations

def read_point(line):
    return tuple(map(int, line.replace(',',' ').split()))

def manhattan(a, b):
    return (abs(a[0]-b[0]) + abs(a[1]-b[1])
                + abs(a[2]-b[2]) + abs(a[3]-b[3]))

def count_constellations(points):
    point_constellations = {}
    for a,b in combinations(points,2):
        if manhattan(a,b) <= 3:
            ca = point_constellations.get(a)
            cb = point_constellations.get(b)
            if ca==cb:
                if not ca:
                    ca = {a,b}
                    point_constellations[a] = point_constellations[b] = ca
            elif ca and cb:
                ca.update(cb)
                for k in cb:
                    point_constellations[k] = ca
            elif ca:
                ca.add(b)
                point_constellations[b] = ca
            elif cb:
                cb.add(a)
                point_constellations[a] = cb
    constellations = set(map(frozenset, point_constellations.values()))
    remaining = frozenset(points) - frozenset.union(*constellations)
    return len(constellations) + len(remaining)

def main():
    points = [read_point(ln) for ln in sys.stdin.read().strip().splitlines()]
    print("Num constellations:", count_constellations(points))

if __name__ == '__main__':
    main()
