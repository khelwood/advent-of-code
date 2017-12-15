#!/usr/bin/env python3

import sys

from knothash import Loop
from collections import deque

sys.path.append('..')
from point import Point
from grid import Grid

def make_maze(key, height):
    maze = Grid(128, height, '.')
    for y in range(height):
        loop = Loop()
        loop.apply_input('%s-%s'%(key, y))
        x = 0
        for num in loop.densehash():
            for i in range(8):
                if (num&(1<<(7-i))):
                    maze[x+i, y] = '#'
            x += 8
    return maze

def grid_find(grid, value, start=Point(0,0)):
    x0, y0 = start
    for y in range(y0, grid.height):
        for x in range(x0, grid.width):
            if grid[x,y]==value:
                return Point(x,y)
        x0 = 0
    return None

def count_regions(grid):
    count = 0
    p = grid_find(grid, '#')
    while p is not None:
        count += 1
        flood(grid, '.', p)
        p = grid_find(grid, '#', p)
    return count

def flood(grid, value, p):
    oldvalue = grid[p]
    queue = deque()
    queue.append(p)
    while queue:
        p = queue.popleft()
        if grid[p]!=oldvalue:
            continue
        x0 = p.x
        while x0 > 0 and grid[x0-1, p.y]==oldvalue:
            x0 -= 1
        x1 = p.x+1
        while x1 < grid.width and grid[x1, p.y]==oldvalue:
            x1 += 1
        for x in range(x0, x1):
            q = Point(x, p.y)
            above = q - (0,1)
            below = q + (0,1)
            if above in grid and grid[above]==oldvalue:
                queue.append(above)
            if below in grid and grid[below]==oldvalue:
                queue.append(below)
            grid[q] = value

def make_knot_hash(key, index):
    loop = Loop()
    loop.apply_input('%s-%s'%(key, index))
    return loop.knothash()

def main():
    if len(sys.argv)<=1:
        exit("Usage: %s <key>"%sys.argv[0])
    print("Building maze...")
    key = sys.argv[1]
    maze = make_maze(key, 128)
    count = maze.data.count('#')
    print("Used count:", count)
    regions = count_regions(maze)
    print("Num regions:", regions)

if __name__ == '__main__':
    main()
