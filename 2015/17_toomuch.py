#!/usr/bin/env python3

import sys

def iter_combinations(sizes, total):
    if total==0:
        yield ()
        return
    if len(sizes)==1:
        if total==sizes[0]:
            yield (total,)
        return
    size = sizes[0]
    rest = sizes[1:]
    yield from iter_combinations(rest, total)
    if size <= total:
        size_tuple = (size,)
        for combo in iter_combinations(rest, total-size):
            yield size_tuple + combo

def main():
    total = 150
    sizes = list(map(int, sys.stdin.read().split()))
    n = 0
    ml = len(sizes)
    mlcount = 0
    for combo in iter_combinations(sizes, total):
        n += 1
        if len(combo) < ml:
            ml = len(combo)
            mlcount = 1
        elif len(combo)==ml:
            mlcount += 1
    print("Number of combinations:", n)
    print("Minimum combination length:", ml)
    print("Number of length %s combinations: %s"%(ml, mlcount))

if __name__ == '__main__':
    main()
