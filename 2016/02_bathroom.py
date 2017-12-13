#!/usr/bin/env python3

import sys
sys.path.append('..')

from point import Point
from grid import Grid

DIGITS = '123456789ABCD'

DIRECTIONS = { 'U': Point(0,-1), 'D': Point(0,1),
                   'L': Point(-1,0), 'R': Point(1, 0) }

def make_first_grid():
    grid = Grid(3,3)
    i = 1
    for y in range(grid.height):
        for x in range(grid.width):
            grid[x,y] = str(i)
            i += 1
    return grid

def make_second_grid():
    grid = Grid(5,5,' ')
    i = 0
    x_points = [[2,3], [1,4], [0,5], [1,4], [2,3]]
    for y, xs in enumerate(x_points):
        for x in range(*xs):
            grid[x,y] = DIGITS[i]
            i += 1
    return grid

def grid_find(grid, value):
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[x,y] == value:
                return Point(x,y)

def find_code(grid, lines):
    grid.current = grid_find(grid, '5')
    letters = [run_line(grid, line) for line in lines]
    return ''.join(letters)

def run_line(grid, line):
    for ch in line:
        pos = grid.current + DIRECTIONS[ch]
        if pos in grid and grid[pos]!=' ':
            grid.current = pos
    return grid[grid.current]

def main():
    lines = sys.stdin.read().strip().split('\n')
    grids = [make_first_grid(), make_second_grid()]
    codes = [find_code(grid, lines) for grid in grids]
    for i in range(len(grids)):
        print("\nGrid %s:"%(i+1))
        print(grids[i])
        print("Code:", codes[i])

if __name__ == '__main__':
    main()
