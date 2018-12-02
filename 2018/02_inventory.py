#!/usr/bin/env python3

import sys
from collections import Counter
from itertools import combinations

def main():
    codes = sys.stdin.read().split()
    twos = 0
    threes = 0
    for code in codes:
        vs = Counter(code).values()
        twos += (2 in vs)
        threes += (3 in vs)
    print("Checksum:", twos*threes)
    for a,b in combinations(codes, 2):
        if sum(x!=y for x,y in zip(a,b))==1:
            print("Code pair:",a,b)
            print("Solution:", ''.join(x for x,y in zip(a,b) if x==y))

if __name__ == '__main__':
    main()
