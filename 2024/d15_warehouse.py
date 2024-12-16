#!/usr/bin/env python3

import sys
from dataclasses import dataclass

class Point(tuple):
    @classmethod
    def at(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self,p))
    def __sub__(self, p):
        return Point(a-b for (a,b) in zip(self,p))
    def __neg__(self):
        return Point(-a for a in self)
    def gps(self):
        return 100*self[1] + self[0]


UP,RIGHT,DOWN,LEFT = (Point(p) for p in zip((0,1,0,-1),(-1,0,1,0)))
DIR = dict(zip('^>v<', (UP,RIGHT,DOWN,LEFT)))

@dataclass
class Warehouse:
    walls: set
    boxes: set
    robot: Point
    course: tuple
    def copy(self):
        return Warehouse(set(self.walls), set(self.boxes), self.robot, self.course)

def read_input():
    walls = set()
    boxes = set()
    for y,line in enumerate(map(str.strip, sys.stdin)):
        if not line:
            break
        for x,ch in enumerate(line):
            if ch=='.':
                continue
            p = Point.at(x,y)
            if ch=='#':
                walls.add(p)
            elif ch=='O':
                boxes.add(p)
            elif ch=='@':
                robot = p
    course = []
    for line in filter(bool, map(str.strip, sys.stdin)):
        course += [DIR[ch] for ch in line]
    return Warehouse(walls, boxes, robot, tuple(course))

def advance(wh, d):
    n = wh.robot + d
    if n in wh.walls:
        return
    if n not in wh.boxes:
        wh.robot = n
        return
    p = n + d
    while p in wh.boxes:
        p += d
    if p in wh.walls:
        return
    wh.boxes.add(p)
    wh.boxes.remove(n)
    wh.robot = n

@dataclass
class BigBox:
    pos: Point
    @property
    def left(self):
        return self.pos
    @property
    def right(self):
        return self.pos+RIGHT
    def slide_right(self, grid):
        del grid[self.left]
        self.pos += RIGHT
        grid[self.right] = self
    def slide_left(self, grid):
        del grid[self.right]
        self.pos += LEFT
        grid[self.left] = self
    def slide(self, grid, d):
        match d[0]:
            case 1: return self.slide_right(grid)
            case -1: return self.slide_left(grid)
        for p in self:
            del grid[p]
        self.pos += d
        for p in self:
            grid[p] = self
    def __hash__(self):
        return id(self)
    def __eq__(self, other):
        return self is other
    def __iter__(self):
        yield self.pos
        yield self.pos + RIGHT


def widen_grid(wh):
    def widen(p):
        return Point.at(p[0]*2, p[1])
    grid = {widen(p):'#' for p in wh.walls}
    grid.update({widen(p)+RIGHT:'#' for p in wh.walls})
    boxes = [BigBox(widen(p)) for p in wh.boxes]
    for box in boxes:
        grid[box.left] = box
        grid[box.right] = box
    robot = widen(wh.robot)
    return grid, robot, boxes

def advance_wide(grid, robot, d):
    n = robot + d
    if n not in grid:
        return n
    if grid[n]=='#':
        return robot
    if d[1]==0: # horizontal
        boxes = [grid[n]]
        d2 = d+d
        p = n+d2
        while (v := grid.get(p)):
            if v=='#':
                return robot
            boxes.append(v)
            p += d2
        for box in reversed(boxes):
            box.slide(grid, d)
        return n
    box_stack = {grid[n]}
    boxes = set()
    while box_stack:
        box = box_stack.pop()
        if box in boxes:
            continue
        boxes.add(box)
        for p in box:
            v = grid.get(p+d)
            if v=='#':
                return robot
            if not v or v in boxes:
                continue
            box_stack.add(v)
    if len(boxes) > 1:
        boxes = sorted(boxes, key=(lambda box:box.pos[1]), reverse=d[1]>0)
    for box in boxes:
        box.slide(grid, d)
    return n

def main():
    wh = read_input()
    grid, robot, boxes = widen_grid(wh)
    for d in wh.course:
        advance(wh, d)
    print(sum(p.gps() for p in wh.boxes))
    for d in wh.course:
        robot = advance_wide(grid, robot, d)
    print(sum(p.pos.gps() for p in boxes))

if __name__ == '__main__':
    main()
