#!/usr/bin/env python3

import sys
import re

sys.path.append('..')

from grid import Grid

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

def bounds(stars):
    star = stars[0]
    (x0,y0) = (x1,y1) = (star.x, star.y)
    for star in stars:
        x = star.x
        y = star.y
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return x0,y0,x1,y1

def display(stars):
    x0,y0,x1,y1 = bounds(stars)
    x1 += 1
    y1 += 1
    grid = Grid(x1-x0, y1-y0, fill='.')
    for star in stars:
        grid[star.x-x0, star.y-y0] = '#'
    for row in grid.rows():
        print(''.join(row))

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
