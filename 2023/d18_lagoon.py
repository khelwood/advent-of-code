#!/usr/bin/env python3

import sys
import re

from typing import NamedTuple

ORDER_PTN = re.compile(r'([RDLU]) (\d+) \(#(\w+)\)')

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self[0]+other[0], self[1]+other[1])

    def __mul__(self, k):
        return Point(self[0]*k, self[1]*k)

    __rmul__ = __mul__

    def __repr__(self):
        return f'({self.x},{self.y})'

DIRECTIONS = {'U':Point(0,-1), 'R':Point(1,0), 'D':Point(0,1), 'L':Point(-1,0)}

HEX_DIR = {k:DIRECTIONS[v] for k,v in ('0R', '1D', '2L', '3U')}

class Order(NamedTuple):
    dir: Point
    distance: int
    colour: str

    def revised(self):
        c = self.colour
        dist = int(c[:-1], 16)
        dir = HEX_DIR[c[-1]]
        return Order(dir, dist, '')


def parse_order(line):
    m = ORDER_PTN.match(line)
    if not m:
        raise ValueError(repr(line))
    dir = DIRECTIONS[m.group(1)]
    distance = int(m.group(2))
    colour = m.group(3)
    return Order(dir, distance, colour)

def follow(orders):
    cur = Point(0,0)
    points = []
    for order in orders:
        cur += order.distance*order.dir
        points.append(cur)
    return points

def shoelace(points):
    total = 0
    last = points[-1]
    for p in points:
        total += last[0]*p[1] - p[0]*last[1]
        last = p
    return total//2

def count_boundary(orders):
    return sum(o.distance for o in orders)

def calculate_area(orders):
    points = follow(orders)
    sl = shoelace(points)
    p = count_boundary(orders)
    return sl + p//2 + 1


def main():
    orders = list(map(parse_order, sys.stdin.read().strip().splitlines()))
    print("Part 1:", calculate_area(orders))
    orders = [order.revised() for order in orders]
    print("Part 2:", calculate_area(orders))

if __name__ == '__main__':
    main()
