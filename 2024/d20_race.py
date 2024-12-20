#!/usr/bin/env python3

import sys

class Point(tuple):
    @classmethod
    def at(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for a,b in zip(self,p))

DIRS = tuple(map(Point, zip((1,0,-1,0),(0,1,0,-1))))

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class Maze:
    def __init__(self, wid, hei, walls, start, end):
        self.wid = wid
        self.hei = hei
        self.walls = walls
        self.start = start
        self.end = end

    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)

    def open(self, p):
        return p in self and p not in self.walls

    def open_neighbours(self, p):
        for d in DIRS:
            n = p+d
            if self.open(n):
                yield n

    def wall_neighbours(self, p):
        for d in DIRS:
            n = p+d
            if n in self.walls:
                yield n

def read_maze():
    walls = set()
    for y,line in enumerate(filter(bool, map(str.strip, sys.stdin))):
        for x,ch in enumerate(line):
            if ch=='.':
                continue
            p = Point.at(x,y)
            if ch=='#':
                walls.add(p)
            elif ch=='S':
                start = p
            elif ch=='E':
                end = p
    return Maze(x+1, y+1, walls, start, end)

def scan_maze(maze):
    steps = 0
    new = [maze.end]
    score = {}
    while new:
        cur = new
        new = []
        for p in cur:
            if score.get(p, steps+1) <= steps:
                continue
            score[p] = steps
            for n in maze.open_neighbours(p):
                new.append(n)
        steps += 1
    return score

def find_short_cheats(maze, scores):
    cheats = set()
    for p,sc in scores.items():
        if sc >= 102:
            for w in maze.wall_neighbours(p):
                for n in maze.open_neighbours(w):
                    if scores.get(n, sc) <= sc-102:
                        cheats.add((n,p))
    return cheats

def find_long_cheats(maze, score):
    sorted_points = sorted(score, key=score.get)
    cheats = set()
    for p in sorted_points:
        sc = score[p]
        if sc < 102:
            continue
        for q in sorted_points:
            dsc = sc - score[q]
            if dsc < 102:
                break
            dist = manhattan(p,q)
            if dist > 20 or dsc - dist < 100:
                continue
            cheats.add((p,q))
    # I thought I was going to have to check that endpoints of
    # the cheat are actually adjacent to walls that the cheat
    # passes through, but I got the right answer without that check.
    return cheats

def main():
    maze = read_maze()
    score = scan_maze(maze)
    par = score[maze.start]
    cheats = find_short_cheats(maze, score)
    print(len(cheats))
    cheats = find_long_cheats(maze, score)
    print(len(cheats))

if __name__ == '__main__':
    main()
