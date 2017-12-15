#!/usr/bin/env python3

import sys

from collections import namedtuple

Alternative = namedtuple('Alternative', 'dir sign')

def read_alt(alt):
    delta = -1 if alt.startswith('-') else 1
    return Alternative(alt.lstrip('+-'), delta)

def sign(n):
    return (1 if n>1 else -1 if n<0 else 0)

class Direction:
    def __init__(self, name, opposite, alts):
        self.name = name
        self.opposite = opposite
        self.alts = [read_alt(alt) for alt in alts.split()]
    def apply(self, loc, delta):
        if (sign(loc[self.name]) != -delta
                and any(sign(loc[alt.dir])==-delta*alt.sign
                            for alt in self.alts)):
            for alt in self.alts:
                loc[alt.dir] += delta*alt.sign
        else:
            loc[self.name] += delta

DIRECTIONS = (
    Direction('n', 's', '+nw +ne'),
    Direction('ne', 'sw', '-nw +n'),
    Direction('nw', 'se', '-ne +n'),
)

DIR_DICT = { d.name: (d,1) for d in DIRECTIONS }
DIR_DICT.update({ d.opposite: (d,-1) for d in DIRECTIONS })

def track_distance(split_data):
    loc = { d.name: 0 for d in DIRECTIONS }
    most_steps = 0
    for d in split_data:
        direction, delta = DIR_DICT[d]
        direction.apply(loc, delta)
        steps = sum(map(abs, loc.values()))
        if steps > most_steps:
            most_steps = steps

    print("Final distance:", steps)
    print("Greatest distance:", most_steps)
            
    
def main():
    data = sys.stdin.read().replace(',',' ').split()
    track_distance(data)

if __name__ == '__main__':
    main()
