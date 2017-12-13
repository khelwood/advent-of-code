#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

sys.path.append('..')

from point import Point
from grid import Grid

ON = '#'
OFF = '.'

def compile(expr):
    expr = expr.replace(' ',r'\s+').replace('#','([0-9]+)')
    return re.compile('^'+expr+'$')

def fill_rect(grid, width, height):
    for i in range(width):
        for j in range(height):
            grid[i,j] = ON

def rotate_row(grid, y, delta):
    delta %= grid.width
    if delta==0:
        return
    row = [grid[x,y] for x in range(grid.width)]
    for x in range(grid.width):
        grid[x,y] = row[x-delta]

def rotate_column(grid, x, delta):
    delta %= grid.height
    if delta==0:
        return
    column = [grid[x,y] for y in range(grid.height)]
    for y in range(grid.height):
        grid[x,y] = column[y-delta]

Command = namedtuple('Command', 'pattern function')
        
COMMANDS = [ Command(compile(x), y) for (x,y) in
                (('rect #x#', fill_rect),
                 ('rotate row y=# by #', rotate_row),
                 ('rotate column x=# by #', rotate_column))]

def process(grid, line):
    for cmd in COMMANDS:
        m = cmd.pattern.match(line)
        if m:
            return cmd.function(grid, int(m.group(1)), int(m.group(2)))
    raise ValueError(repr(line))

def main():
    lines = sys.stdin.read().strip().split('\n')
    grid = Grid(50, 6, OFF)
    for line in lines:
        process(grid, line)
    count_on = sum(x==ON for x in grid.data)
    print("Count:", count_on)
    print(grid)

if __name__ == '__main__':
    main()
