#!/usr/bin/env python3

import sys
import re

class Nanobot:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    def inrange(self, pos):
        return (manhattan(self.pos, pos) <= self.radius)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def read_bot(line):
    line = line.strip()
    m = re.match('pos = < # , # , # > , r = # $'
                     .replace(' ',r'\s*').replace('#', r'(-?\d+)'), line)
    if not m:
        raise ValueError(repr(line))
    vals = tuple(map(int, m.groups()))
    return Nanobot(vals[:3], vals[3])

def main():
    bots = [read_bot(line) for line in sys.stdin.read().strip().splitlines()]
    strongest = max(bots, key=lambda bot: bot.radius)
    radius = strongest.radius
    inrange = sum(strongest.inrange(bot.pos) for bot in bots)
    print("In range:", inrange)

if __name__ == '__main__':
    main()
