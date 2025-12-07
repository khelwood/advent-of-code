#!/usr/bin/env python3

import sys
from collections import namedtuple, Counter

Grid = namedtuple('Grid', 'hei splits start')

def read_input():
    splits = set()
    for y,line in enumerate(sys.stdin):
        for x,ch in enumerate(line):
            if ch=='^':
                maxy = y
                splits.add((x,y))
            elif ch=='S':
                start = (x,y)
    return Grid(maxy+1, splits, start)

def count_splits(grid):
    nsplits = 0
    x,y = grid.start
    xs = (x,)
    y += 1
    while y < grid.hei:
        newxs = set()
        for x in xs:
            if (x,y) in grid.splits:
                newxs.update((x-1,x+1))
                nsplits += 1
            else:
                newxs.add(x)
        xs = newxs
        y += 1
    return nsplits

def count_paths(grid):
    x,y = grid.start
    xs = {x:1}
    y += 1
    while y < grid.hei:
        newxs = Counter()
        for x,n in xs.items():
            if (x,y) in grid.splits:
                newxs[x-1] += n
                newxs[x+1] += n
            else:
                newxs[x] += n
        xs = newxs
        y += 1
    return sum(xs.values())

def main():
    grid = read_input()
    print(count_splits(grid))
    print(count_paths(grid))

if __name__ == '__main__':
    main()
