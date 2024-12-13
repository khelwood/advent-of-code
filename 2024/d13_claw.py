#!/usr/bin/env python3

# Button A: 3 tokens
# Button B: 1 token

import sys
import re
from dataclasses import dataclass

class Point(tuple):
    @classmethod
    def of(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self, p))
    def __sub__(self, p):
        return Point(a-b for (a,b) in zip(self, p))
    def __neg__(self):
        return Point(-a for a in self)
    def __mul__(self, v):
        return Point(v*a for a in self)
    __rmul__ = __mul__
    def cross(self, p):
        return self[0]*p[1] - p[0]*self[1]

@dataclass
class Prize:
    a: Point
    b: Point
    target: Point

A_COST = 3
B_COST = 1

def read_prizes():
    ptn = re.compile(r'^([a-z ]+):\s*X[+=](\S+),\s*Y[+=](\S+)\s*$', flags=re.I)
    prizes = []
    for line in sys.stdin:
        m = ptn.match(line)
        if not m:
            continue
        p = Point(map(int, (m.group(2), m.group(3))))
        name = m.group(1)
        if name=='Button A':
            a = p
        elif name=='Button B':
            b = p
        else:
            prizes.append(Prize(a,b,p))
    return prizes

def solve(prize, limit=None):
    axb = prize.a.cross(prize.b)
    if axb==0: # None of the input a,b are parallel
        return None
    axt = prize.a.cross(prize.target)
    if axt%axb:
        return None
    nb = axt//axb
    if nb < 0 or limit is not None and nb > limit:
        return None
    r = prize.target - nb*prize.b
    na = r[0]//prize.a[0]
    if na*prize.a!=r or limit is not None and na > limit:
        return None
    return A_COST*na + B_COST*nb

def main():
    prizes = read_prizes()
    print(sum(solve(prize, 100) or 0 for prize in prizes))
    adjustment = Point(2*(10_000_000_000_000,))
    for prize in prizes:
        prize.target += adjustment
    print(sum(solve(prize) or 0 for prize in prizes))

if __name__ == '__main__':
    main()
