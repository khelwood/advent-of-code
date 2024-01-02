#!/usr/bin/env python3

import sys
import re

NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

DIRECTIONS = (EAST, SOUTH, WEST, NORTH)

def turn_left(p):
    return (p[1], -p[0])

def turn_right(p):
    return (-p[1], p[0])

TURNS = {'L':turn_left, 'R':turn_right}

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

class Maze:
    def __init__(self, lines):
        self.wid = max(map(len, lines))
        self.hei = len(lines)
        self.lines = lines
        self.indents = tuple(map(count_indent, lines))
        self.ways = self.make_ways()
        self.start = (lines[0].index('.'), 0)

    def __getitem__(self, p):
        x,y = p
        if (0 <= y < self.hei):
            line = self.lines[y]
            if self.indents[y] <= x < len(line):
                return line[x]
        return ' '

    def line_bounds(self, y):
        return (self.indents[y], len(self.lines[y]))

    def travel(self, p, d):
        ways = self.ways.get(p)
        return ways.get(d) if ways else None

    def make_ways(self):
        ways = {}
        for y,line in enumerate(self.lines):
            x0 = self.indents[y]
            x1 = len(line)
            for x in range(x0, x1):
                if line[x]!='.':
                    continue
                pways = ways[x,y] = {}
                nx = (x1-1 if x==x0 else x-1)
                if line[nx]=='.':
                    pways[WEST] = ((nx,y), WEST)
                nx = (x0 if x==x1-1 else x+1)
                if line[nx]=='.':
                    pways[EAST] = ((nx,y), EAST)
                ny = y+1
                ch = self[x,ny]
                if ch==' ':
                    ny = y
                    while self[x,ny-1]!=' ':
                        ny -= 1
                    ch = self[x,ny]
                if ch=='.':
                    pways[SOUTH] = ((x,ny), SOUTH)
                ny = y-1
                ch = self[x,ny]
                if ch==' ':
                    ny = y
                    while self[x,ny+1]!=' ':
                        ny += 1
                    ch = self[x,ny]
                if ch=='.':
                    pways[NORTH] = ((x,ny), NORTH)
        return ways

    def zip(self, a0, ad, aout, b0, bd, bout, n):
        a = a0
        b = b0
        a_in = (-aout[0], -aout[1])
        b_in = (-bout[0], -bout[1])
        ways = self.ways
        for _ in range(n):
            if self[a]=='.' and self[b]=='.':
                ways[a][aout] = (b,b_in)
                ways[b][bout] = (a,a_in)
            else:
                if a in ways:
                    ways[a].pop(aout, None)
                if b in ways:
                    ways[b].pop(bout, None)
            a = addp(a, ad)
            b = addp(b, bd)


def count_indent(line):
    return next(x for (x,ch) in enumerate(line) if not ch.isspace())

def split_route(line):
    ptn = re.compile(r'(\d+)([LR]?)')
    for a,b in ptn.findall(line):
        yield int(a)
        if b:
            yield b

def follow_route(maze, start, dir, route):
    cur = start
    for r in route:
        if isinstance(r, int):
            for _ in range(r):
                n = maze.travel(cur, dir)
                if n is None:
                    break
                cur,dir = n
        else:
            dir = TURNS[r](dir)
    return cur,dir


def find_corners(maze):
    bds = (x0,x1) = maze.line_bounds(0)
    yield (x0, 0)
    yield (x1-1, 0)
    y = next((y for y in range(maze.hei) if maze.line_bounds(y) != bds), None)
    while y is not None:
        x0,x1 = maze.line_bounds(y)
        if x0 < bds[0]:
            yield (bds[0], y)
            yield (x0, y)
        elif x0 > bds[0]:
            yield (bds[0], y-1)
            yield (x0, y-1)
        if x1 < bds[1]:
            yield (bds[1]-1, y-1)
            yield (x1-1, y-1)
        elif x1 > bds[1]:
            yield (bds[1]-1, y)
            yield (x1-1, y)
        bds = (x0,x1)
        y = next((y for y in range(y+1,maze.hei) if maze.line_bounds(y) != bds), None)
    y = maze.hei-1
    bds = maze.line_bounds(y)
    yield (bds[0],y)
    yield (bds[1]-1,y)

def show_corners(maze):
    lines = list(maze.lines)
    c = ord('A')
    for x,y in find_corners(maze):
        s = lines[y]
        lines[y] = s[:x]+chr(c)+s[x+1:]
        c += 1
    for line in lines:
        print(line)
    for (i,p) in enumerate(find_corners(maze), ord('A')):
        print(chr(i),':',p)

def zip_corners(maze):
    EDGE = 50
    # A s ~ n to F
    maze.zip((50,0), SOUTH, WEST, (0, 149), NORTH, WEST, EDGE)
    # I n ~ w to A
    maze.zip((0,199), NORTH, WEST, (99,0), WEST, NORTH, EDGE)
    # E w ~ E n
    maze.zip((49,100), WEST, NORTH, (50,99), NORTH, WEST, EDGE)
    # B s ~ G n
    maze.zip((149,0), SOUTH, EAST, (99,149), NORTH, EAST, EDGE)
    # G n ~ B s
    maze.zip((99,149), NORTH, EAST, (149,0), SOUTH, EAST, EDGE)
    # D e ~ D s
    maze.zip((100,49), EAST, SOUTH, (99,50), SOUTH, EAST, EDGE)
    # H e ~ H s
    maze.zip((50,149), EAST, SOUTH, (49,150), SOUTH, EAST, EDGE)

def output(p, d):
    x,y = p
    row = y+1
    col = x+1
    d = DIRECTIONS.index(d)
    return 1000*row + 4*col + d

def main():
    lines = list(map(str.rstrip, sys.stdin.read().rstrip().splitlines()))
    i = lines.index('')
    maze = Maze(lines[:i])
    if len(sys.argv)>1 and sys.argv[1]=='c':
        return show_corners(maze)
    route = list(split_route(lines[-1]))
    p,dir = follow_route(maze, maze.start, EAST, route)
    print("Part 1:", output(p, dir))

    zip_corners(maze)
    p,dir = follow_route(maze, maze.start, EAST, route)
    print("Part 2:", output(p, dir))


if __name__ == '__main__':
    main()
