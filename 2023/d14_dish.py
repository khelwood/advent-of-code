#!/usr/bin/env python3

import sys

ROLLS = [ (lambda p: (p[0], p[1]-1), False),
  (lambda p: (p[0]-1, p[1]), False),
  (lambda p: (p[0], p[1]+1), True),
  (lambda p: (p[0]+1, p[1]), True),
]

class Grid:
    def __init__(self, wid, hei, fixed):
        self.wid = wid
        self.hei = hei
        self.fixed = fixed
        # add solid border
        for x in (-1, wid):
            for y in range(hei):
                fixed.add((x,y))
        for y in (-1, hei):
            for x in range(wid):
                fixed.add((x,y))

    def roll(self, rocks, fn, reverse):
        rocks = sorted(rocks, reverse=reverse)
        new_rocks = set()
        for p in rocks:
            q = fn(p)
            while q not in self.fixed and q not in new_rocks:
                p = q
                q = fn(p)
            new_rocks.add(p)
        return new_rocks

    def roll_cycle(self, rocks):
        for fn, reverse in ROLLS:
            rocks = self.roll(rocks, fn, reverse)
        return frozenset(rocks)

    def load(self, rocks):
        return sum((self.hei-y) for (x,y) in rocks)


def read_rocks(lines):
    hei = len(lines)
    wid = len(lines[0])
    rocks = set()
    fixed = set()
    locs = {}
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch == 'O':
                rocks.add((x,y))
            elif ch=='#':
                fixed.add((x,y))
    return frozenset(rocks), Grid(wid, hei, fixed)

def main():
    rocks, grid = read_rocks(sys.stdin.read().strip().splitlines())
    rocks1 = grid.roll(rocks, *ROLLS[0])
    print("Part 1:", grid.load(rocks1))
    num_cycles = 1_000_000_000
    seen = {}
    states = []
    for i in range(num_cycles):
        if rocks in seen:
            repeat_start = seen[rocks]
            period = i - repeat_start
            break
        seen[rocks] = i
        states.append(rocks)
        rocks = grid.roll_cycle(rocks)
    t = (num_cycles - repeat_start)%period
    rocks = states[t+repeat_start]
    print("Part 2:", grid.load(rocks))

if __name__ == '__main__':
    main()
