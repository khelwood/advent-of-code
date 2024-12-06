#!/usr/bin/env python3

import sys

class Maze:
    def __init__(self, wid, hei, walls, start):
        self.wid = wid
        self.hei = hei
        self.walls = walls
        self.start = start
    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def read_maze():
    walls = set()
    for y,line in enumerate(filter(bool, map(str.strip, sys.stdin))):
        for x,ch in enumerate(line):
            if ch=='#':
                walls.add((x,y))
            elif ch=='^':
                start = (x,y)
    return Maze(x+1, y+1, walls, start)

def turn_right(dire):
    return (-dire[1], dire[0])

def trace_route(maze):
    pos = maze.start
    visited = set()
    dire = (0,-1)
    while pos in maze:
        visited.add(pos)
        np = addp(pos, dire)
        while np in maze.walls:
            dire = turn_right(dire)
            np = addp(pos, dire)
        pos = np
    return visited

def loops(maze):
    stances = set()
    pos = maze.start
    dire = (0,-1)
    while pos in maze:
        stance = (pos, dire)
        if stance in stances:
            return True
        stances.add(stance)
        np = addp(pos, dire)
        while np in maze.walls:
            dire = turn_right(dire)
            np = addp(pos, dire)
        pos = np
    return False

def block_loops(maze, visited):
    n = 0
    visited.remove(maze.start)
    for p in visited:
        maze.walls.add(p)
        if loops(maze):
            n += 1
        maze.walls.remove(p)
    return n

def main():
    maze = read_maze()
    visited = trace_route(maze)
    print(len(visited))
    print(block_loops(maze, visited))

if __name__ == '__main__':
    main()
