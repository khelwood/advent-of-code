#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

sys.path.append('..')
from grid import Grid

@dataclass
class Claim:
    id: int
    left: int
    top: int
    width: int
    height: int
    def __iter__(self):
        yrange = range(self.top, self.top + self.height)
        for x in range(self.left, self.left + self.width):
            for y in yrange:
                yield (x,y)

CLAIM_PTN = re.compile('#% @ %,%: %x%$'
                           .replace(' ', r'\s+')
                           .replace('%', r'(\d+)'))

def make_claim(line):
    m = CLAIM_PTN.match(line)
    if not m:
        raise ValueError(repr(line))
    d = [int(x) for x in m.groups()]
    return Claim(id=d[0], left=d[1], top=d[2], width=d[3], height=d[4])

def main():
    claims = [make_claim(line) for line in sys.stdin.read().splitlines()]
    grid = Grid(1000, 1000, fill=0)
    for claim in claims:
        for p in claim:
            grid[p] += 1
    overlapcount = sum(v > 1 for v in grid.values())
    print("Overlap count:", overlapcount)
    for claim in claims:
        for p in claim:
            if grid[p] > 1:
                break
        else:
            print("Correct claim:", claim)

if __name__ == '__main__':
    main()
