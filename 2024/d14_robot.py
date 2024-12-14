#!/usr/bin/env python3

import sys
import re
import operator
from functools import reduce
from dataclasses import dataclass

WID=101
HEI=103
CX = WID//2
CY = HEI//2

class Point(tuple):
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self,p))
    def __sub__(self, p):
        return Point(a-b for (a,b) in zip(self,p))
    def __neg__(self):
        return Point(-a for a in self)
    def __mul__(self, v):
        return Point(a*v for a in self)
    __rmul__ = __mul__

@dataclass
class Robot:
    p: Point
    v: Point
    def travel(self, time):
        x = (self.p.x + time*self.v.x)%WID
        y = (self.p.y + time*self.v.y)%HEI
        self.p = Point((x,y))
        return self.p
    def quadrant(self):
        xd = self.p.x - CX
        if xd==0:
            return None
        yd = self.p.y - CY
        if yd==0:
            return None
        return (0 if xd < 0 else 1) + (0 if yd < 0 else 2)

def read_robots():
    ptn = re.compile(r'^p=#,#\s*v=#,#\s*$'.replace('#', r'(-?\d+)'))
    robots = []
    for line in sys.stdin:
        m = ptn.match(line)
        if m:
            p = Point(int(m.group(i)) for i in (1,2))
            v = Point(int(m.group(i)) for i in (3,4))
            robots.append(Robot(p,v))
    return robots

def multiply(seq):
    return reduce(operator.mul, seq, 1)

def count_quadrants(robots):
    quadrant_counts = {i:0 for i in range(4)}
    for r in robots:
        q = r.quadrant()
        if q is not None:
            quadrant_counts[q] += 1
    return quadrant_counts

def progress(robots, time=1):
    for r in robots:
        r.travel(time)

def xmas(robots):
    positions = {r.p for r in robots}
    if any(all((x,y) in positions for x in range(CX-10,CX+10)) for y in range(HEI)):
        return True

def display(robots):
    positions = {robot.p for robot in robots}
    for y in range(HEI):
        for x in range(WID):
            print('X' if (x,y) in positions else '.', end='')
        print()

def main():
    robots = read_robots()
    og_robots = [Robot(r.p, r.v) for r in robots]
    progress(robots, 100)
    quadrant_counts = count_quadrants(robots)
    print(multiply(quadrant_counts.values()))
    robots = og_robots
    time = 0
    while not xmas(robots):
        progress(robots)
        time += 1
    display(robots)
    print(time)

if __name__ == '__main__':
    main()
