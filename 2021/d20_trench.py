#!/usr/bin/env python3

import sys
from itertools import product
from dataclasses import dataclass

ALL_BITS = 511

@dataclass
class Grid:
    marks : set
    default : bool

    def compute_region(self, pos):
        total = 0
        bit = 1
        marks = self.marks
        for nbr in ordered_neighbours(pos):
            if nbr in marks:
                total |= bit
            bit <<= 1
        if self.default:
            total = ALL_BITS ^ total
        return total

    def find_bounds(self):
        x0 = 1_000_000
        x1 = 0
        y0 = 1_000_000
        y1 = 0
        for x,y in self.marks:
            x0 = min(x0, x)
            x1 = max(x1, x)
            y0 = min(y0, y)
            y1 = max(y1, y)
        return x0,y0,x1,y1

    def enhance(self, code):
        new = set()
        newdefault = code[ALL_BITS if self.default else 0]
        x0,y0,x1,y1 = self.find_bounds()
        for pos in product(range(x0-1, x1+2), range(y0-1,y1+2)):
            region = self.compute_region(pos)
            if code[region]!=newdefault:
                new.add(pos)
        return Grid(new, newdefault)

    def __len__(self):
        return len(self.marks)

def ordered_neighbours(pos):
    x,y = pos
    yield (x+1,y+1)
    yield (x,y+1)
    yield (x-1,y+1)
    yield (x+1,y)
    yield (x,y)
    yield (x-1,y)
    yield (x+1,y-1)
    yield (x,y-1)
    yield (x-1,y-1)

def read_input():
    lines = sys.stdin.read().strip().splitlines()
    code = [ch=='#' for ch in lines.pop(0)]
    while not lines[0]:
        del lines[0]

    marks = set()
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                marks.add((x,y))
    return code, Grid(marks, False)

def main():
    code, grid = read_input()
    for _ in range(2):
        grid = grid.enhance(code)
    print('After 2:  ', len(grid))
    for _ in range(2, 50):
        grid = grid.enhance(code)
    print('After 50:', len(grid))

if __name__ == '__main__':
    main()
