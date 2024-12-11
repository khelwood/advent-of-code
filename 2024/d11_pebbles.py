#!/usr/bin/env python3

import sys
from collections import Counter

def output(v, cache={0:(1,)}):
    o = cache.get(v)
    if o is not None:
        return o
    sv = str(v)
    lv = len(sv)
    if lv%2==0:
        hl = lv//2
        o = (int(sv[:hl]), int(sv[hl:]))
    else:
        o = (2024*v,)
    cache[v] = o
    return o

def advance(counts):
    out = Counter()
    for k,c in counts.items():
        for v in output(k):
            out[v] += c
    return out

def main():
    counts = Counter(map(int, sys.stdin.read().split()))
    for _ in range(25):
        counts = advance(counts)
    print(sum(counts.values()))
    for _ in range(50):
        counts = advance(counts)
    print(sum(counts.values()))

if __name__ == '__main__':
    main()
