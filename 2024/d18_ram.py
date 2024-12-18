#!/usr/bin/env python3

import sys

class Point(tuple):
    @classmethod
    def at(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self,p))

class Grid:
    def __init__(self, walls, wid, hei):
        self.walls = walls
        self.wid = wid
        self.hei = hei

    def __contains__(self, p):
        x,y = p
        return (0 <= x < self.wid and 0 <= y < self.hei)

    def open(self, p):
        return (p in self and p not in self.walls)

    def print(self):
        for y in range(self.hei):
            print(''.join('#' if (x,y) in self.walls else '.' for x in range(self.wid)))

DIRS = tuple(map(Point, zip((1,0,-1,0), (0,1,0,-1))))

def read_input():
    positions = []
    for line in filter(bool, map(str.strip, sys.stdin)):
        x,_,y = line.partition(',')
        positions.append(Point(map(int, (x,y))))
    return positions

def scan_grid(grid, target):
    scores = {}
    new_points = [target]
    score = 0
    while new_points:
        cur_points = new_points
        new_points = []
        for pos in cur_points:
            if scores.get(pos, score+1) <= score:
                continue
            scores[pos] = score
            for d in DIRS:
                n = pos + d
                if grid.open(n) and scores.get(n, score+1) > score:
                    new_points.append(n)
        score += 1
    return scores

def find_blocker(grid, start, target, new_walls):
    for wall in new_walls:
        grid.walls.add(wall)
        scores = scan_grid(grid, target)
        if start not in scores:
            return wall
    return None

def main():
    positions = read_input()
    if all(v <= 6 for p in positions for v in p):
        wid = hei = 7
        falls = 12
    else:
        wid = hei = 71
        falls = 1024
    walls = set(positions[:falls])
    grid = Grid(walls, wid, hei)
    start = Point.at(0, 0)
    target = Point.at(wid-1, hei-1)
    scores = scan_grid(grid, target)
    print(scores[start])
    print(find_blocker(grid, start, target, positions[falls:]))

if __name__ == '__main__':
    main()
