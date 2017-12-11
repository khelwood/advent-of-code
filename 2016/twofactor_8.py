#!/usr/bin/env python3

import sys
sys.path.append('..')

from point import Point
from grid import Grid

import re
import pyperclip

ON = '#'
OFF = '.'

def _compile(expr):
    expr = expr.replace(' ',r'\s+').replace('#','([0-9]+)')
    return re.compile('^'+expr+'$')

def fill_rect(grid, width, height):
    print(f"fill_rect({width},{height})")
    for i in range(width):
        for j in range(height):
            grid[i,j] = ON

def rotate_row(grid, y, delta):
    print(f"rotate_row({y},{delta})")
    delta %= grid.width
    if delta==0:
        return
    row = [grid[x,y] for x in range(grid.width)]
    for x in range(grid.width):
        grid[x,y] = row[x-delta]

def rotate_column(grid, x, delta):
    print(f"rotate_column({x},{delta})")
    delta %= grid.height
    if delta==0:
        return
    column = [grid[x,y] for y in range(grid.height)]
    for y in range(grid.height):
        grid[x,y] = column[y-delta]

PATTERNS = [(_compile(x),y) for x,y in
                (('rect #x#', fill_rect),
                     ('rotate row y=# by #', rotate_row),
                     ('rotate column x=# by #', rotate_column))]

def process(grid, line):
    print(grid)
    for pattern,fn in PATTERNS:
        m = pattern.match(line)
        if m:
            return fn(grid, int(m.group(1)), int(m.group(2)))
    raise ValueError("Unprocessed line: %r"%line)


def main():
    grid = Grid(50, 6, OFF)
    print("Copy instructions to clipboard and press enter.")
    input()
    block = pyperclip.paste().strip()
    lines = block.split('\n')
    for line in lines:
        process(grid, line)
    print(grid)
    count_on = sum(x==ON for x in grid)
    print("Count:", count_on)
    
    

if __name__ == '__main__':
    main()
