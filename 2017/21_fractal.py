#!/usr/bin/env python3

import sys

from collections import namedtuple

sys.path.append('..')
from grid import Grid

def sub_grids(grid):
    block_size = 2 + grid.width%2
    for y0 in range(0, grid.height, block_size):
        for x0 in range(0, grid.width, block_size):
            yield tuple(''.join([grid[x, y] for x in range(x0, x0+block_size)])
                            for y in range(y0, y0+block_size))

def enhance(grid, enhancements):
    new_size = 4*grid.width//3 if grid.width%2 else 3*grid.width//2
    new_grid = Grid(new_size, new_size, '.')
    block_size = 3 + grid.width%2
    sources = sub_grids(grid)
    for y0 in range(0, new_size, block_size):
        for x0 in range(0, new_size, block_size):
            source = next(sources)
            result = enhancements[source]
            for y, line in enumerate(result):
                for x, ch in enumerate(line):
                    new_grid[x+x0, y+y0] = ch
    return new_grid

def read_enhancements(lines):
    results = {}
    for line in lines:
        k,v = map(str.strip, line.split('=>'))
        k,v = [tuple(x.split('/')) for x in (k,v)]
        results[k] = v
    return results

def rotate_lines(lines):
    return tuple(''.join([line[i] for line in reversed(lines)])
                     for i in range(len(lines)))

def enhance_enhancements(enhancements):
    for k,v in list(enhancements.items()):
        enhancements[k[::-1]] = v
        for _ in range(3):
            k = rotate_lines(k)
            enhancements[k] = v
            enhancements[k[::-1]] = v

def main():
    lines = sys.stdin.read().strip().split('\n')
    enhancements = read_enhancements(lines)
    enhance_enhancements(enhancements)
    grid = Grid(3,3,'.')
    grid[1,0] = grid[2,1] = grid[0,2] = grid[1,2] = grid[2,2] = '#'
    print(grid)
    for i in range(5):
        grid = enhance(grid, enhancements)
        print("Enhancement", i+1)
        print(grid)
    count = grid.data.count('#')
    print("Number on after 5:", count)
    for i in range(13):
        print(" (%s)"%(i+6), end='\r')
        grid = enhance(grid, enhancements)
    count = grid.data.count('#')
    print("Number on after 18:", count)

if __name__ == '__main__':
    main()
