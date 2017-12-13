#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

# Part 2
EXTRA_LINE = 'Disc #7 has 11 positions; at time=0, it is at position 0.'

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

def process(lines):
    discs = read_discs(lines)
    period = max(d.num_pos for d in discs)
    d = next(d for d in discs if d.num_pos==period)
    drop_time = (d.num_pos - d.start_pos - d.index)%period
    while not all(d.position_for(drop_time)==0 for d in discs):
        drop_time += period
    print("Time:",drop_time)

def main():
    lines = sys.stdin.read().strip().split('\n')
    process(lines)
    lines.append(EXTRA_LINE)
    process(lines)

if __name__ == '__main__':
    main()
