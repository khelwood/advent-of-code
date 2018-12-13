#!/usr/bin/env python3

import sys
import re

from collections import namedtuple, defaultdict

ON = '#'
OFF = '.'
WIDTH = 50
HEIGHT = 6

Command = namedtuple('Command', 'pattern function')
Command.commands = []

def command(expr):
    expr = '^' + expr.replace(' ',r'\s+').replace('#','([0-9]+)') + '$'
    def command(func):
        Command.commands.append(Command(re.compile(expr), func))
        return func
    return command

@command('rect #x#')
def fill_rect(grid, width, height):
    for i in range(width):
        for j in range(height):
            grid[i,j] = ON

@command('rotate row y=# by #')
def rotate_row(grid, y, delta, wid=WIDTH):
    delta %= wid
    if delta==0:
        return
    row = [grid[x,y] for x in range(wid)]
    for x in range(wid):
        grid[x,y] = row[x-delta]

@command('rotate column x=# by #')
def rotate_column(grid, x, delta, hei=HEIGHT):
    delta %= hei
    if delta==0:
        return
    column = [grid[x,y] for y in range(hei)]
    for y in range(hei):
        grid[x,y] = column[y-delta]

def process(grid, line):
    for cmd in Command.commands:
        m = cmd.pattern.match(line)
        if m:
            args = [int(g) for g in m.groups()]
            return cmd.function(grid, *args)
    raise ValueError(repr(line))

def display(grid, wid=WIDTH, hei=HEIGHT):
    for y in range(hei):
        print(' '.join([grid[x,y] for x in range(wid)]))

def main():
    lines = sys.stdin.read().strip().split('\n')
    grid = defaultdict(lambda: OFF)
    for line in lines:
        process(grid, line)
    count_on = sum(v==ON for v in grid.values())
    print("Count:", count_on)
    display(grid)

if __name__ == '__main__':
    main()
