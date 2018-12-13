#!/usr/bin/env python3

import sys
import itertools
from collections import deque

from knothash import Loop

sys.path.append('..')
from point import Point

WIDTH = HEIGHT = 128

def make_maze(key, wid=WIDTH, hei=HEIGHT):
    maze = { p:'.' for p in itertools.product(range(wid), range(hei)) }
    for y in range(hei):
        loop = Loop()
        loop.apply_input('%s-%s'%(key, y))
        x = 0
        for num in loop.densehash():
            for i in range(8):
                if (num&(1<<(7-i))):
                    maze[x+i, y] = '#'
            x += 8
    return maze

def grid_find(grid, value, start=Point(0,0), wid=WIDTH, hei=HEIGHT):
    x0, y0 = start
    for y in range(y0, hei):
        for x in range(x0, wid):
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

def flood(grid, value, p, wid=WIDTH, hei=HEIGHT):
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
        while x1 < wid and grid[x1, p.y]==oldvalue:
            x1 += 1
        for x in range(x0, x1):
            q = Point(x, p.y)
            above = q - (0,1)
            below = q + (0,1)
            if grid.get(above)==oldvalue:
                queue.append(above)
            if grid.get(below)==oldvalue:
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
    maze = make_maze(key)
    count = sum(v=='#' for v in maze.values())
    print("Used count:", count)
    regions = count_regions(maze)
    print("Num regions:", regions)

if __name__ == '__main__':
    main()
