#!/usr/bin/env python3

import sys

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

def next_value_simple(layout, pos):
    x,y = pos
    value = layout[pos]
    if value==EMPTY:
        for xx in (x-1, x, x+1):
            for yy in (y-1, y, y+1):
                if layout[xx,yy]==OCCUPIED:
                    return value
        return OCCUPIED
    if value==OCCUPIED:
        count = 0
        for xx in (x-1, x, x+1):
            for yy in (y-1, y, y+1):
                if layout[xx,yy]==OCCUPIED:
                    count += 1
                    if count >= 5:
                        return EMPTY
    return value

def next_value_long(layout, pos):
    value = layout[pos]
    if value==EMPTY:
        if any(v==OCCUPIED for v in long_adjacent(layout, pos)):
            return value
        return OCCUPIED
    if value==OCCUPIED:
        count = 0
        for v in long_adjacent(layout, pos):
            if v==OCCUPIED:
                count += 1
                if count >= 5:
                    return EMPTY
    return value


def long_adjacent(layout, pos):
    x,y = pos
    xx = x-1
    yy = y-1
    width = layout.width
    height = layout.height
    while xx >= 0 and yy >= 0:
        value = layout[xx,yy]
        if value!=FLOOR:
            yield value
            break
        xx -= 1
        yy -= 1
    xx = x-1
    while xx >= 0:
        value = layout[xx,y]
        if value != FLOOR:
            yield value
            break
        xx -= 1
    xx = x-1
    yy = y+1
    while xx >= 0 and yy < height:
        value = layout[xx,yy]
        if value != FLOOR:
            yield value
            break
        xx -= 1
        yy += 1
    yy = y+1
    while yy < height:
        value = layout[x,yy]
        if value != FLOOR:
            yield value
            break
        yy += 1
    xx = x+1
    yy = y+1
    while xx < width and yy < height:
        value = layout[xx,yy]
        if value != FLOOR:
            yield value
            break
        xx += 1
        yy += 1
    xx = x+1
    while xx < width:
        value = layout[xx,y]
        if value != FLOOR:
            yield value
            break
        xx += 1
    xx = x+1
    yy = y-1
    while xx < width and yy >= 0:
        value = layout[xx,yy]
        if value != FLOOR:
            yield value
            break
        xx += 1
        yy -= 1
    yy = y-1
    while yy >= 0:
        value = layout[x,yy]
        if value != FLOOR:
            yield value
            break
        yy -= 1

class Layout:
    def __init__(self, width, height):
        self.grid = {}
        self.width = width
        self.height = height
        self.next_value_function = next_value_simple

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
        func = self.next_value_function
        return {pos:func(self, pos) for pos in self.grid}


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
    while True:
        old = layout.grid
        layout.advance_grid()
        if layout.grid==old:
            break
    print("Number of occupied seats (simple):", layout.count(OCCUPIED))

    layout.grid = original_grid
    layout.next_value_function = next_value_long
    while True:
        old = layout.grid
        layout.advance_grid()
        if layout.grid==old:
            break
    print("Number of occupied seats (long):", layout.count(OCCUPIED))

if __name__ == '__main__':
    main()
