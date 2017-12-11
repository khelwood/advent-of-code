#!/usr/bin/env python3

import re
from collections import namedtuple
import itertools

LINES = """Disc #1 has 17 positions; at time=0, it is at position 15.
Disc #2 has 3 positions; at time=0, it is at position 2.
Disc #3 has 19 positions; at time=0, it is at position 4.
Disc #4 has 13 positions; at time=0, it is at position 2.
Disc #5 has 7 positions; at time=0, it is at position 2.
Disc #6 has 5 positions; at time=0, it is at position 0.""".split('\n')

# Part 2
LINES.append('Disc #7 has 11 positions; at time=0, it is at position 0.')

DISC_PTN = re.compile(
    '^Disc #% has % positions; at time=0, it is at position %.$'
    .replace('%', r'([0-9]+)')
)
Disc = namedtuple('Disc', 'index num_pos start_pos')

Disc.position_for = lambda self, drop_time: (
    drop_time + self.index + self.start_pos)%self.num_pos

def _match(ptn, line):
    m = ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    return m

def read_disc(line):
    m = _match(DISC_PTN, line)
    di, npos, initpos = (int(m.group(i)) for i in range(1,4))
    return Disc(di, npos, initpos)

def read_discs(lines):
    return [read_disc(line) for line in lines]
    
def main():
    discs = read_discs(LINES)
    period = max(d.num_pos for d in discs)
    d = next(d for d in discs if d.num_pos==period)
    drop_time = (d.num_pos - d.start_pos - d.index)%period
    while not all(d.position_for(drop_time)==0 for d in discs):
        drop_time += period
    print("Time:",drop_time)
    

if __name__ == '__main__':
    main()
