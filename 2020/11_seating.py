#!/usr/bin/env python3

import sys

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

def adjacent_simple(layout, pos):
    grid = layout.grid
    x,y = pos
    for xx in (x-1, x, x+1):
        for yy in (y-1, y, y+1):
            p = (xx,yy)
            if p in grid and p!=pos:
                yield p

def adjacent_long(layout, pos):
    grid = layout.grid
    width = layout.width
    height = layout.height
    x,y = pos
    xx = x-1
    yy = y-1
    while xx >= 0 and yy >= 0:
        p = (xx,yy)
        if p in grid:
            yield p
            break
        xx -= 1
        yy -= 1
    xx = x-1
    while xx >= 0:
        p = (xx,y)
        if p in grid:
            yield p
            break
        xx -= 1
    xx = x-1
    yy = y+1
    while xx >= 0 and yy < height:
        p = (xx,yy)
        if p in grid:
            yield p
            break
        xx -= 1
        yy += 1
    yy = y+1
    while yy < height:
        p = (x,yy)
        if p in grid:
            yield p
            break
        yy += 1
    xx = x+1
    yy = y+1
    while xx < width and yy < height:
        p = (xx,yy)
        if p in grid:
            yield p
            break
        xx += 1
        yy += 1
    xx = x+1
    while xx < width:
        p = (xx,y)
        if p in grid:
            yield p
            break
        xx += 1
    xx = x+1
    yy = y-1
    while xx < width and yy >= 0:
        p = (xx,yy)
        if p in grid:
            yield p
            break
        xx += 1
        yy -= 1
    yy = y-1
    while yy >= 0:
        p = (x, yy)
        if p in grid:
            yield p
            break
        yy -= 1


class Layout:
    def __init__(self, width, height):
        self.grid = {}
        self.width = width
        self.height = height

    def find_adjacent_seats(self, function):
        self.adj = {pos:list(function(self, pos)) for pos in self.grid}

    def __getitem__(self, pos):
        return self.grid.get(pos, FLOOR)

    def __setitem__(self, pos, value):
        x,y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            if value==FLOOR:
                self.grid.pop(pos, None)
            else:
                self.grid[pos] = value
        else:
            raise ValueError(pos)

    def count(self, value):
        return sum(v==value for v in self.grid.values())

    def advance_grid(self):
        self.grid = self.next_grid()

    def next_grid(self):
        func = self.next_value
        return {pos:func(pos) for pos in self.grid}

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
    grid = layout.grid
    for y,line in enumerate(lines):
        for x,value in enumerate(line):
            if value != FLOOR:
                grid[x,y] = value
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
