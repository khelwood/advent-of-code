#!/usr/bin/env python3

import sys

def parse_input(line):
    return [(int(a), int(b)) for (a,_,b) in
            (p.partition('-') for p in line.strip().split(','))]

def sum_range_invalid_1(minv, maxv):
    lmx = len(str(maxv))
    lmn = len(str(minv))
    c = 0
    while lmn != lmx:
        d = 10**lmn
        c += sum_range_invalid_1(minv, d-1)
        minv = d
        lmn = len(str(minv))
    if lmx % 2 != 0:
        return c
    nfirst = int(str(minv)[:lmn//2])
    mult = 10**(lmx//2) + 1
    if nfirst * mult < minv:
        nfirst += 1
    nlast = int(str(maxv)[:lmx//2])
    if nlast * mult > maxv:
        nlast -= 1
    c += ((nfirst + nlast) * (1 + nlast - nfirst) // 2) * mult
    return c

def setup_mults():
    mults = {}
    for n in range(2,11):
        vals = []
        for f in range(1, n//2+1):
            if n%f==0:
                v = (str(10**(f-1))*(n//f)).rstrip('0')
                vals.append((int(v), f))
        mults[n] = tuple(vals)
    return mults

MULTS = setup_mults()

def sum_range_invalid_2(minv, maxv):
    lmx = len(str(maxv))
    if lmx == 1:
        return 0
    lmn = len(str(minv))
    c = 0
    while lmn != lmx:
        d = 10**lmn
        c += sum_range_invalid_2(minv, d-1)
        minv = d
        lmn = len(str(minv))
    mults = MULTS.get(lmx)
    if mults is None:
        return c
    invalid = set()
    for mult, sl in mults:
        nfirst = int(str(minv)[:sl])
        v = nfirst*mult
        if v < minv:
            v += mult
        while v <= maxv:
            invalid.add(v)
            v += mult
    return c + sum(invalid)

def main():
    ranges = parse_input(sys.stdin.read())
    print(sum(sum_range_invalid_1(a,b) for (a,b) in ranges))
    print(sum(sum_range_invalid_2(a,b) for (a,b) in ranges))

if __name__ == '__main__':
    main()
