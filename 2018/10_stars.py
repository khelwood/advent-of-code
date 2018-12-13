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

def bounds(positions):
    x0 = min(x for (x,y) in positions)
    y0 = min(y for (x,y) in positions)
    x1 = max(x for (x,y) in positions)
    y1 = max(y for (x,y) in positions)
    return x0,y0, x1,y1

def stars_area(stars):
    x0,y0, x1,y1 = bounds(tuple((star.x, star.y) for star in stars))
    return (y1-y0) * (x1-x0)

def display(stars):
    positions = {(star.x, star.y) for star in stars}
    x0,y0, x1,y1 = bounds(positions)
    xran = range(x0,x1+1)
    for y in range(y0,y1+1):
        print(''.join(['#' if (x,y) in positions else '.' for x in xran]))

def main():
    stars = [read_star(line) for line in sys.stdin.read().splitlines()]
    leftmost = min(stars, key=lambda star: star.x)
    rightmost = max(stars, key=lambda star: star.x)
    distance = rightmost.x-leftmost.x-80 # get them all near enough to draw
    speed = leftmost.vx-rightmost.vx
    time = distance//speed
    for star in stars:
        star.advance(time)
    last_area = stars_area(stars)
    # Find the point when the stars are all closest together
    while True:
        for star in stars:
            star.advance(1)
        area = stars_area(stars)
        if area > last_area:
            for star in stars:
                star.advance(-1)
            break
        last_area = area
    display(stars)
    print("Time:", time)

if __name__ == '__main__':
    main()
