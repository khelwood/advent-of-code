#!/usr/bin/env python3

import sys
import re

class Star:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def advance(self, steps=1):
        self.x += self.vx*steps
        self.y += self.vy*steps

INPUT_PTN = re.compile(r'[^<>]*< # , # >[^<>]*< # , # >'
                          .replace(' ', r'\s*')
                          .replace('#', r'(-?\d+)'))

def read_star(line, ptn=INPUT_PTN):
    m = ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    return Star(*map(int, m.groups()))

def display(stars):
    positions = {(star.x, star.y) for star in stars}
    x0 = min(x for (x,y) in positions)
    y0 = min(y for (x,y) in positions)
    x1 = max(x for (x,y) in positions)
    y1 = max(y for (x,y) in positions)
    xran = range(x0,x1+1)
    for y in range(y0,y1+1):
        print(''.join(['#' if (x,y) in positions else '.' for x in xran]))

def main():
    stars = [read_star(line) for line in sys.stdin.read().splitlines()]
    leftmost = min(stars, key=lambda star: star.x)
    rightmost = max(stars, key=lambda star: star.x)
    distance = rightmost.x-leftmost.x-50 # get all the stars near enough to draw
    speed = leftmost.vx-rightmost.vx
    time = distance//speed
    for star in stars:
        star.advance(time)
    display(stars)
    print("Time:", time)
    # Somehow I hit the correct second first time

if __name__ == '__main__':
    main()
