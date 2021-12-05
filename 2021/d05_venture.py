#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from collections import Counter

def birange(a, b):
    return range(a, b+1) if a <= b else range(a, b-1, -1)

@dataclass
class Vent:
    start: (int,int)
    end: (int,int)
    @property
    def orthoganal(self):
        return (self.start[0]==self.end[0] or self.start[1]==self.end[1])
    def __iter__(self):
        x0,y0 = self.start
        x1,y1 = self.end
        if x0==x1:
            return ((x0,y) for y in birange(y0,y1))
        if y0==y1:
            return ((x,y0) for x in birange(x0, x1))
        return zip(birange(x0,x1), birange(y0,y1))

def read_vent(line, ptn=re.compile(r'^#,# -> #,#$'.replace('#',r'(\d+)'))):
    m = ptn.match(line)
    coords = tuple(int(g) for g in m.groups())
    return Vent(coords[:2], coords[2:])

def main():
    vents = [read_vent(line) for line in sys.stdin.read().strip().splitlines()]
    orth_vents = [vent for vent in vents if vent.orthoganal]
    point_counter = Counter(p for vent in orth_vents for p in vent)
    overlaps = sum(v > 1 for v in point_counter.values())
    print("Overlaps in orthoganal vents:", overlaps)
    point_counter = Counter(p for vent in vents for p in vent)
    overlaps = sum(v > 1 for v in point_counter.values())
    print("Overlaps including diagonal vents:", overlaps)

if __name__ == '__main__':
    main()
