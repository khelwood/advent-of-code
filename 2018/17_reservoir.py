#!/usr/bin/env python3

import sys
import re
import itertools

class Ground:
    def __init__(self, clay, spring):
        self.positions = {p:'#' for p in clay}
        self.spring = spring
        self.find_bounds()
    def __getitem__(self, pos):
        return self.positions.get(pos, '.')
    def __setitem__(self, pos, value):
        self.positions[pos] = value

    def settled(self, x,y):
        return self[x,y] in '~#'

    def find_bounds(self):
        self.x0 = min(x for x,y in self.positions)
        self.x1 = max(x for x,y in self.positions) + 1
        self.y0 = min(y for x,y in self.positions)
        self.y1 = max(y for x,y in self.positions) + 1

    def display(self):
        xran = range(self.x0, self.x1)
        for y in range(self.y0, self.y1):
            print(''.join([self[x,y] for x in xran]))

    def fill(self):
        new_springs = {self.spring}
        positions = self.positions
        while new_springs:
            springs = new_springs
            new_springs = set()
            for sx,sy in springs:
                for y in range(max(sy, self.y0), self.y1):
                    v = self[sx,y]
                    if v=='.':
                        self[sx,y] = '|'
                        continue
                    if v in '~#':
                        for spr in self.fill_from(sx, y-1):
                            new_springs.add(spr)
                        break

    def fill_from(self, sx, sy, flowing='|'):
        while True:
            self[sx,sy] = flowing
            left = sx
            while self.settled(left-1, sy+1) and not self.settled(left-1, sy):
                left -= 1
                self[left,sy] = flowing
            right = sx
            while self.settled(right+1, sy+1) and not self.settled(right+1, sy):
                right += 1
                self[right,sy] = flowing
            leftwall = (left-1) if self.settled(left-1, sy) else None
            rightwall = (right+1) if self.settled(right+1, sy) else None
            if leftwall is None:
                self[left-1, sy] = flowing
                yield (left-1, sy)
            if rightwall is None:
                self[right+1, sy] = flowing
                yield (right+1, sy)
            if not (leftwall and rightwall):
                return
            for x in range(left, right+1):
                self[x, sy] = '~'
            sy -= 1

    def count(self, value):
        return sum(v==value for v in self.positions.values())

def recomp(expr):
    return re.compile(expr.replace(' ', r'\s*').replace('#', r'(\d+)') + '$')

def range_from_expr(expr, p1=recomp(r'\w = #'), p2=recomp(r'\w = # \.\. #')):
    m = p1.match(expr)
    if m:
        return (int(m.group(1)),)
    m = p2.match(expr)
    if m:
        return range(int(m.group(1)), int(m.group(2))+1)
    raise ValueError(repr(expr))

def addp(a, b):
    return (a[0]+b[0], a[1]+b[1])

def read_clay():
    clay = set()
    for line in sys.stdin:
        xr,yr = map(range_from_expr, sorted(map(str.strip, line.split(','))))
        clay.update(itertools.product(xr, yr))
    return clay

def main():
    clay = read_clay()
    ground = Ground(clay, (500,0))
    print(ground.x0, ground.y0, ground.x1, ground.y1)
    ground.fill()
    flowing = ground.count('|')
    settled = ground.count('~')
    print("Water count:", flowing+settled)
    print("Settled count:", settled)

if __name__ == '__main__':
    main()
