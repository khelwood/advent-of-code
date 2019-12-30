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
    def __init__(self, grid, portals, start, end):
        self.grid = grid
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

def parse_maze(data):
    pos_letter = {}
    grid = {}
    for y,line in enumerate(data.splitlines()):
        for x,value in enumerate(line):
            if value.isalpha():
                pos_letter[x,y] = value
            elif value==SPACE_S:
                grid[x,y] = value

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

    return Maze(grid, portals, start, end)

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

def portal_locations(grid, pos):
    return [nbr for nbr in neighbours(pos) if grid.get(nbr)==SPACE_S]

def draw_maze(maze):
    grid = maze.grid
    y0 = min(y for (_,y) in grid)
    y1 = max(y for (_,y) in grid)
    x0 = min(x for (x,_) in grid)
    x1 = max(x for (x,_) in grid)
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            value = grid.get((x,y), ' ')
            if isinstance(value, int) and value >= 10:
                value = chr(ord('A') + value - 10)
            print(value, end='')
        print()
    print("Start:", maze.start)
    print("End:", maze.end)
    print("Portals:", maze.portals)

def main():
    data = sys.stdin.read().rstrip()
    maze = parse_maze(data)
    draw_maze(maze)
    maze.route = make_route(maze, maze.start)
    distance = maze.route[maze.end]
    print("Distance to end:", distance)

if __name__ == '__main__':
    main()
