#!/usr/bin/env python3

import sys
import re
import itertools
from collections import Counter, namedtuple

Claim = namedtuple('Claim', 'id left top width height')
Claim.__iter__ = lambda self : itertools.product(
            range(self.left, self.left + self.width),
            range(self.top, self.top + self.height)
        )

def make_claim(line, ptn=re.compile('#%@%,%:%x%$'.replace('%', r'(\d+)'))):
    m = ptn.match(re.sub(r'\s+','',line))
    if not m:
        raise ValueError(repr(line))
    return Claim(*map(int, m.groups()))

def main():
    claims = [make_claim(line) for line in sys.stdin.read().splitlines()]
    land = Counter()
    for claim in claims:
        land.update(claim)
    overlapcount = sum(v > 1 for v in land.values())
    print("Overlap count:", overlapcount)
    for claim in claims:
        if all(land[p] <= 1 for p in claim):
            print("Correct claim ID:", claim.id)

if __name__ == '__main__':
    main()
