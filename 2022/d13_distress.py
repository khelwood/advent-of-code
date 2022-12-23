#!/usr/bin/env python3

import sys
from functools import cmp_to_key
from ast import literal_eval as leval

def read_input():
    it = iter(sys.stdin)
    for line in it:
        line = line.strip()
        if not line:
            continue
        a = leval(line)
        b = leval(next(it))
        yield (a,b)

def cmp(a,b):
    aint = isinstance(a, int)
    bint = isinstance(b, int)
    if aint and bint:
        return a - b
    if aint:
        a = [a]
    if bint:
        b = [b]
    for ai, bi in zip(a,b):
        c = cmp(ai, bi)
        if c:
            return c
    return len(a) - len(b)


def main():
    pairs = list(read_input())
    total = 0
    for i,(a,b) in enumerate(pairs, 1):
        if cmp(a,b) <= 0:
            total += i
    print("Total:", total)
    dividers = [ [[2]], [[6]] ]
    pairs = [x for pair in pairs for x in pair] + dividers
    pairs.sort(key=cmp_to_key(cmp))
    x,y = [pairs.index(div)+1 for div in dividers]
    key = x*y
    print("Key:", key)


if __name__ == '__main__':
    main()
