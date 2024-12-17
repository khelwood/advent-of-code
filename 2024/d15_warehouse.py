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

class Widehouse(Warehouse):
    def __getitem__(self, p):
        if p in self.walls:
            return '#'
        if p in self.boxes:
            return p
        p += LEFT
        if p in self.boxes:
            return p
        return None
    def slide(self, box, d):
        self.boxes.remove(box)
        self.boxes.add(box+d)

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
        return wh.robot
    if n not in wh.boxes:
        return n
    p = n + d
    while p in wh.boxes:
        p += d
    if p in wh.walls:
        return wh.robot
    wh.boxes.add(p)
    wh.boxes.remove(n)
    return n

def widen_warehouse(wh):
    def widen(p):
        return Point.at(p[0]*2, p[1])
    walls = {widen(p) for p in wh.walls}|{widen(p)+RIGHT for p in wh.walls}
    boxes = {widen(p) for p in wh.boxes}
    robot = widen(wh.robot)
    return Widehouse(walls, boxes, robot, wh.course)

def advance_wide(wh, d):
    n = wh.robot + d
    v = wh[n]
    if not v:
        return n
    if v=='#':
        return wh.robot
    box = v
    if d[1]==0: # horizontal
        boxes = [box]
        d2 = d+d
        p = n + d2
        while (v := wh[p]):
            if v=='#':
                return wh.robot
            boxes.append(v)
            p += d2
        for box in reversed(boxes):
            wh.slide(box, d)
        return n
    box_stack = {box}
    boxes = set()
    while box_stack:
        box = box_stack.pop()
        if box in boxes:
            continue
        boxes.add(box)
        for p in (box, box+RIGHT):
            v = wh[p+d]
            if v=='#':
                return wh.robot
            if not v or v in boxes:
                continue
            box_stack.add(v)
    if len(boxes) > 1:
        boxes = sorted(boxes, key=(lambda box:box[1]), reverse=d[1]>0)
    for box in boxes:
        wh.slide(box, d)
    return n

def main():
    wh = read_input()
    wide = widen_warehouse(wh)
    for d in wh.course:
        wh.robot = advance(wh, d)
    print(sum(p.gps() for p in wh.boxes))
    for d in wide.course:
        wide.robot = advance_wide(wide, d)
    print(sum(p.gps() for p in wide.boxes))

if __name__ == '__main__':
    main()
