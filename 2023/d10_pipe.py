#!/usr/bin/env python3

import sys
import re

from typing import NamedTuple
from dataclasses import dataclass

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self[0]+other[0], self[1]+other[1])

    def __sub__(self, other):
        return Point(self[0]-other[0], self[1]-other[1])

    def __neg__(self):
        return Point(-self[0], -self[1])


@dataclass
class Grid:
    lines: list
    start: Point

    @property
    def wid(self):
        return len(self.lines[0])

    @property
    def hei(self):
        return len(self.lines)

    def __getitem__(self, pos):
        x,y = pos
        return self.lines[y][x]

    def __setitem__(self, pos, ch):
        x,y = pos
        line = self.lines[y]
        self.lines[y] = line[:x] + ch + line[x+1:]

    def get(self, pos, default=None):
        if pos not in self:
            return default
        return self[pos]

    def pipe_neighbours(self, pos):
        ch = self.get(pos)
        if ch is None:
            return ()
        joins = JOINS[ch]
        if joins:
            return [pos+d for d in joins]
        return ()

    def __iter__(self):
        return (Point(x,y) for (y,x) in product(range(self.hei), range(self.wid)))

    def __contains__(self, p):
        x,y = p
        return 0 <= x < self.wid and 0 <= y < self.hei


NORTH = Point(0,-1)
EAST = Point(1,0)
SOUTH = Point(0,1)
WEST = Point(-1,0)
DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

JOINS = {
    '|':(NORTH,SOUTH),
    '-':(WEST,EAST),
    'L':(NORTH,EAST),
    'J':(NORTH,WEST),
    'F':(EAST,SOUTH),
    '7':(WEST,SOUTH),
    '.':(),
    'S':(),
}

def parse_maze(text):
    data = {}
    lines = text.splitlines()
    for y,line in enumerate(lines):
        x = line.find('S')
        if x >= 0:
            start = Point(x, y)
            break
    grid = Grid(lines, start)
    start_dirs = set()
    for d in DIRECTIONS:
        nbr = start + d
        if start in grid.pipe_neighbours(nbr):
            start_dirs.add(nbr-start)
    ch = next(c for c,j in JOINS.items() if set(j)==start_dirs)
    grid[start] = ch
    return grid

def trace_route(grid):
    start = grid.start
    route = [start]
    cur = next(iter(grid.pipe_neighbours(start)))
    while cur != start:
        prev = route[-1]
        route.append(cur)
        cur = next(p for p in grid.pipe_neighbours(cur) if p!=prev)
    return route

def clear_junk(maze, boundary):
    lines = maze.lines
    for y,line in enumerate(lines):
        line = list(line)
        for x,ch in enumerate(line):
            if Point(x,y) not in boundary:
                line[x] = '.'
        lines[y] = ''.join(line)

def count_inside(maze):
    count = 0
    for line in maze.lines:
        inside = False
        line = re.sub(r'F-*J|L-*7', '|', line)
        for x,ch in enumerate(line):
            if ch=='|':
                inside = not inside
            elif inside and ch=='.':
                count += 1
    return count


def main():
    maze = parse_maze(sys.stdin.read())
    route = trace_route(maze)
    furthest = len(route)//2
    print('Part 1:', furthest)
    clear_junk(maze, set(route))
    count = count_inside(maze)
    print('Part 2:', count)

if __name__ == '__main__':
    main()
