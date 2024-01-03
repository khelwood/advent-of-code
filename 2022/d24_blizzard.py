#!/usr/bin/env python3

import sys
import math

from dataclasses import dataclass

NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

DIRECTIONS = {'^':NORTH, '>':EAST, 'v':SOUTH, '<':WEST}

def addp(p, d):
    return (p[0]+d[0], p[1]+d[1])

@dataclass
class Grid:
    wid: int
    hei: int
    walls: set
    blizzards: dict
    start: tuple
    end: tuple

    def project_blizzard(self, pos, dir):
        np = addp(pos, dir)
        if np in self.walls:
            if dir==NORTH:
                np = (np[0], self.hei-2)
            elif dir==SOUTH:
                np = (np[0], 1)
            elif dir==EAST:
                np = (1, np[1])
            elif dir==WEST:
                np = (self.wid-2, np[1])
        return np

    def advance(self):
        old = self.blizzards
        new = self.blizzards = {}
        for p,ds in old.items():
            for d in ds:
                np = self.project_blizzard(p,d)
                v = new.get(np)
                if v:
                    v.add(d)
                else:
                    new[np] = {d}

    def open(self, pos):
        x,y = pos
        if not (0 <= x < self.wid and 0 <= y < self.hei):
            return False
        return (pos not in self.walls and pos not in self.blizzards)


def read_grid(lines):
    walls = set()
    blizzards = {}
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                walls.add((x,y))
            elif ch!='.':
                blizzards[x,y] = {DIRECTIONS[ch]}
    start = (lines[0].index('.'),0)
    end = (lines[-1].index('.'), len(lines)-1)
    return Grid(len(lines[0]), len(lines), walls, blizzards, start, end)

def next_move(grid, pos, *, moves=(WEST, NORTH, (0,0), SOUTH, EAST)):
    for move in moves:
        np = addp(pos, move)
        if grid.open(np):
            yield np

def score_spaces(grid, blizzard_seq, start, end, steps):
    period = len(blizzard_seq)
    visited = {(grid.start, steps%period)}
    new_ps = [start]
    while new_ps:
        steps += 1
        bs = steps%period
        grid.blizzards = blizzard_seq[bs]
        old_ps = new_ps
        new_ps = []
        for p in old_ps:
            for np in next_move(grid, p):
                if np==end:
                    return steps
                key = (np, bs)
                if key not in visited:
                    visited.add(key)
                    new_ps.append(np)

def main():
    lines = sys.stdin.read().strip().splitlines()
    grid = read_grid(lines)
    period = math.lcm(grid.wid-2, grid.hei-2)
    blizzard_seq = [grid.blizzards]
    for _ in range(period-1):
        grid.advance()
        blizzard_seq.append(grid.blizzards)
    steps = score_spaces(grid, blizzard_seq, grid.start, grid.end, 0)
    print("Part 1:", steps)
    steps = score_spaces(grid, blizzard_seq, grid.end, grid.start, steps)
    steps = score_spaces(grid, blizzard_seq, grid.start, grid.end, steps)
    print("Part 2:", steps)


if __name__ == '__main__':
    main()
