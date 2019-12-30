#!/usr/bin/env python3

import sys
from collections import defaultdict

SPACE_S = '.'
START_CODE='AA'
END_CODE='ZZ'

def neighbours(pos):
    x,y = pos
    yield (x, y-1)
    yield (x, y+1)
    yield (x-1, y)
    yield (x+1, y)

class Maze:
    def __init__(self, grid, width, height, portals, start, end):
        self.grid = grid
        self.width = width
        self.height = height
        self.portals = portals
        self.start = start
        self.end = end
    def adjacent_spaces(self, pos):
        grid = self.grid
        for nbr in neighbours(pos):
            if nbr in grid:
                yield nbr
        val = grid[pos]
        if isinstance(val, int):
            pp0, pp1 = self.portals[val]
            yield (pp1 if pp0==pos else pp0)
    def adjacent_3D(self, pos):
        grid = self.grid
        px,py,pz = pos
        xy = (px,py)
        for nbr in neighbours(xy):
            if nbr in grid:
                yield nbr + (pz,)
        val = grid[xy]
        if isinstance(val, int):
            inner = (xy in self.inner_portals)
            if pz==0 and not inner:
                return
            pp0, pp1 = self.portals[val]
            pp = (pp1 if pp0==xy else pp0)
            if inner:
                yield pp + (pz+1,)
            else:
                yield pp + (pz-1,)

def parse_maze(data):
    pos_letter = {}
    grid = {}
    width = None
    for y,line in enumerate(data.splitlines()):
        if width is None:
            width = len(line)
        for x,value in enumerate(line):
            if value.isalpha():
                pos_letter[x,y] = value
            elif value==SPACE_S:
                grid[x,y] = value
    height = y+1

    code_pos = defaultdict(list)

    while pos_letter:
        pos,letter = next(iter(pos_letter.items()))
        del pos_letter[pos]
        pos2 = next(p for p in neighbours(pos) if p in pos_letter)
        letter2 = pos_letter[pos2]
        del pos_letter[pos2]
        if pos2 < pos:
            code = letter2 + letter
            pos, pos2 = pos2, pos
        else:
            code = letter + letter2
        code_pos[code].extend((pos, pos2))

    portals = []
    for code, positions in code_pos.items():
        portal_loc = [p for pos in positions
                          for p in portal_locations(grid, pos)]
        if code==START_CODE:
            assert len(portal_loc)==1
            start = portal_loc[0]
            continue
        if code==END_CODE:
            assert len(portal_loc)==1
            end = portal_loc[0]
            continue
        pi = len(portals)
        for pos in portal_loc:
            grid[pos] = pi
        portals.append(portal_loc)

    return Maze(grid, width, height, portals, start, end)

def make_route(maze, start):
    grid = maze.grid
    route = { start: 0 }
    new = [start]
    steps = 0
    while new:
        old = new
        new = []
        steps += 1
        for p in old:
            for nbr in maze.adjacent_spaces(p):
                if nbr not in route:
                    route[nbr] = steps
                    new.append(nbr)
    return route

def distance_3D(maze, start, end):
    assert len(start)==3
    grid = maze.grid
    route = {start: 0}
    new = [start]
    steps = 0
    while new:
        old = new
        new = []
        steps += 1
        for p in old:
            for nbr in maze.adjacent_3D(p):
                if nbr not in route:
                    route[nbr] = steps
                    if nbr==end:
                        return steps
                    new.append(nbr)

def portal_locations(grid, pos):
    return [nbr for nbr in neighbours(pos) if grid.get(nbr)==SPACE_S]

def draw_maze(maze):
    grid = maze.grid
    for y in range(maze.height):
        for x in range(maze.width):
            value = grid.get((x,y), ' ')
            if isinstance(value, int) and value >= 10:
                value = chr(ord('A') + value - 10)
            print(value, end='')
        print()
    print("Start:", maze.start)
    print("End:", maze.end)
    print("Portals:", maze.portals)

def find_inner_portals(maze):
    x0 = 3
    x1 = maze.width-3
    y0 = 3
    y1 = maze.height-3
    inner = set()
    for pi,poss in enumerate(maze.portals):
        for (x,y) in poss:
            if x0 < x < x1 and y0 < y < y1:
                inner.add((x,y))
    return inner

def main():
    data = sys.stdin.read().rstrip()
    maze = parse_maze(data)
    draw_maze(maze)
    route = make_route(maze, maze.start)
    distance = route[maze.end]
    print("Distance flat:", distance)
    maze.inner_portals = find_inner_portals(maze)
    distance = distance_3D(maze, maze.start+(0,), maze.end+(0,))
    print("Distance 3D:", distance)

if __name__ == '__main__':
    main()
