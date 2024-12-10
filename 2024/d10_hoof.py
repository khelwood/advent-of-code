#!/usr/bin/env python3

import sys
from itertools import product
from collections import Counter

class Point(tuple):
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self,p))

DIRS = (Point((1,0)), Point((0,1)), Point((-1,0)), Point((0,-1)))

class Grid:
    def __init__(self, lines):
        self.data = {(x,y):int(ch) for y,line in enumerate(lines)
                    for x,ch in enumerate(line)}
        self.wid = len(lines[0])
        self.hei = len(lines)
    def __getitem__(self, p):
        return self.data.get(p, -1)
    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)
    def find_height(self, h):
        return (Point(p) for p in product(range(self.wid), range(self.hei))
                if self.data[p]==h)

def read_grid():
    lines = list(filter(bool, map(str.strip, sys.stdin)))
    return Grid(lines)

def neighbours(p):
    return (p+d for d in DIRS)

def find_endpoints(grid, p):
    nexts = [p]
    while nexts:
        cur = nexts
        nexts = []
        for p in cur:
            h = grid[p]
            if h == 9:
                continue
            for np in neighbours(p):
                if grid[np]==h+1:
                    nexts.append(np)
    return {p for p in cur if grid[p]==9}

def find_ratings(grid):
    ratings = Counter()
    nexts = set()
    for p in grid.find_height(8):
        for n in neighbours(p):
            if grid[n]==9:
                ratings[p] += 1
            elif grid[n]==7:
                nexts.add(n)
    while nexts:
        cur = nexts
        nexts = set()
        for p in cur:
            h = grid[p]
            for n in neighbours(p):
                if grid[n]==h+1:
                    ratings[p] += ratings[n]
                elif grid[n]==h-1:
                    nexts.add(n)
    return ratings

def main():
    grid = read_grid()
    total_score = sum(len(find_endpoints(grid, p)) for p in grid.find_height(0))
    print(total_score)
    ratings = find_ratings(grid)
    total_rating = sum(ratings[p] for p in grid.find_height(0))
    print(total_rating)

if __name__ == '__main__':
    main()
