#!/usr/bin/env python3

import sys
import itertools

DIRECTIONS = { 'U': (0,-1), 'D': (0,1), 'L': (-1,0), 'R': (1,0) }

def addpoint(a,b):
    return (a[0]+b[0], a[1]+b[1])

def make_first_keypad():
    prod = itertools.product(range(3), range(3))
    return {(x,y): str(i) for (i,(y,x)) in enumerate(prod, 1)}

def make_second_keypad(DIGITS = '123456789ABCD'):
    grid = {}
    digiter = iter(DIGITS)
    x_points = ((2,3), (1,4), (0,5), (1,4), (2,3))
    for y, xs in enumerate(x_points):
        for x in range(*xs):
            grid[x,y] = next(digiter)
    return grid

def find_code(grid, lines):
    cur = next(k for (k,v) in grid.items() if v=='5')
    for line in lines:
        cur = run_line(grid, line, cur)
        yield grid[cur]

def run_line(grid, line, cur):
    for ch in line:
        pos = addpoint(cur, DIRECTIONS[ch])
        if pos in grid and grid[pos]!=' ':
            cur = pos
    return cur

def main():
    lines = sys.stdin.read().strip().split('\n')
    grids = [make_first_keypad(), make_second_keypad()]
    codes = [find_code(grid, lines) for grid in grids]
    for grid in grids:
        print('Code:', ''.join(find_code(grid, lines)))

if __name__ == '__main__':
    main()
