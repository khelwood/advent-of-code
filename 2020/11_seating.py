#!/usr/bin/env python3

import sys

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

DIRECTIONS = ((-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0))

def adjacent_simple(layout, pos):
    grid = layout.grid
    x,y = pos
    for dx,dy in DIRECTIONS:
        p = (x + dx, y + dy)
        if p in grid:
            yield p

def adjacent_long(layout, pos):
    grid = layout.grid
    width = layout.width
    height = layout.height
    x,y = pos
    for dx,dy in DIRECTIONS:
        xx = x+dx
        yy = y+dy
        while 0 <= xx < width and 0 <= yy < height:
            p = (xx,yy)
            if p in grid:
                yield p
                break
            xx += dx
            yy += dy

class Layout:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def find_adjacent_seats(self, function):
        self.adj = {pos:list(function(self, pos)) for pos in self.grid}

    def count(self, value):
        return sum(v==value for v in self.grid.values())

    def advance_grid(self):
        func = self.next_value
        self.grid = {pos:func(pos) for pos in self.grid}

    def next_value(self, pos):
        grid = self.grid
        value = grid[pos]
        if value==EMPTY:
            if any(grid[p]==OCCUPIED for p in self.adj[pos]):
                return value
            return OCCUPIED
        if value==OCCUPIED:
            req = self.threshold
            for p in self.adj[pos]:
                if grid[p]==OCCUPIED:
                    req -= 1
                    if req <= 0:
                        return EMPTY
        return value


def parse_layout(string):
    lines = string.splitlines()
    width = len(lines[0])
    height = len(lines)
    layout = Layout(width, height)
    grid = {}
    for y,line in enumerate(lines):
        for x,value in enumerate(line):
            if value != FLOOR:
                grid[x,y] = value
    layout.grid = grid
    return layout


def main():
    layout = parse_layout(sys.stdin.read().strip())
    original_grid = dict(layout.grid)
    layout.threshold = 4
    layout.find_adjacent_seats(adjacent_simple)
    while True:
        old = layout.grid
        layout.advance_grid()
        if layout.grid==old:
            break
    print("Number of occupied seats (simple):", layout.count(OCCUPIED))

    layout.grid = original_grid
    layout.threshold = 5
    layout.find_adjacent_seats(adjacent_long)
    while True:
        old = layout.grid
        layout.advance_grid()
        if layout.grid==old:
            break
    print("Number of occupied seats (long):", layout.count(OCCUPIED))


if __name__ == '__main__':
    main()
