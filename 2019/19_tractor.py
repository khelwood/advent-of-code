#!/usr/bin/env python3

import sys
import itertools
import math

from intcode import Program, parse_program_input

def find_affected(width, height):
    return { pos for pos in itertools.product(range(width), range(height))
             if in_tractor(*pos) }

def in_tractor(x, y, _cache={}):
    pos = (x,y)
    result = _cache.get(pos)
    if result is not None:
        return result
    prog = Program(prog_input)
    prog.input_values = [x,y]
    prog.execute()
    result = bool(prog.output_values[-1])
    _cache[pos] = result
    return result

def maxc(a,b):
    return a if (b is None or a is not None and a > b) else b

def minc(a, b):
    return a if (b is None or a is not None and b > a) else b

def bilinear(function, minx=None, maxx=None, guess=None):
    """Find the value for which the function returns true,
    but the previous value returns false."""
    if (minx is None or maxx is None) and guess is None:
        raise TypeError("Missing min/max or guess for bilinear")
    if minx is None:
        while True:
            if not function(guess):
                minx = guess
                break
            maxx = maxc(maxx, guess)
            guess //= 2
    if maxx is None:
        while True:
            if function(guess):
                maxx = guess
                break
            minx = guess
            guess *= 2
    while minx + 1 < maxx:
        guess = (minx + maxx) // 2
        if function(guess):
            maxx = guess
        else:
            minx = guess
    if minx + 1 != maxx:
        raise ValueError("Somehow ended up with (minx,maxx) of %r in bilinear."
                             %((minx, maxx)))
    return maxx


def find_initial_angle():
    size = 20
    ratios = []
    for x in range(size):
        if in_tractor(x, size):
            ratios.append(x/size)
    for y in range(1, size):
        if in_tractor(size, y):
            ratios.append(size/y)
    return sum(ratios) / len(ratios)

def find_upper_angle(angle0):
    y = 200
    function = lambda x : in_tractor(x, y)
    x = bilinear(function, guess=angle0*y)
    return x/y

def square_fits(y0, angle1, width, height):
    x1 = int(y0 * angle1)
    if in_tractor(x1, y0):
        x1 += 1
        while in_tractor(x1, y0):
            x1 += 1
    else:
        while not in_tractor(x1-1, y0):
            x1 -= 1
    return in_tractor(x1 - width, y0 + height - 1)

def square_coords(y0, angle1, width, height):
    x1 = int(y0 * angle1)
    if in_tractor(x1, y0):
        x1 += 1
        while in_tractor(x1, y0):
            x1 += 1
    else:
        while not in_tractor(x1-1, y0):
            x1 -= 1
    assert in_tractor(x1-width, y0 + height - 1)
    return (x1-width, y0)

def draw_grid(affected, width, height):
    for y in range(height):
        for x in range(width):
            value = '#' if (x,y) in affected else '.'
            print(value, end='')
        print()

def main():
    global prog_input
    prog_input = parse_program_input(sys.stdin.read())
    print(len(find_affected(50, 50)))
    draw_grid(find_affected(50, 50), 50, 50)
    initial_angle = find_initial_angle()
    print("[initial angle: %s]"%initial_angle)
    angle1 = find_upper_angle(initial_angle)
    print("[upper angle: %s]"%angle1)
    sf = lambda y0: square_fits(y0, angle1, 100, 100)
    y = bilinear(sf, guess=200)
    print("best y:", y)
    assert square_fits(y, angle1, 100, 100)
    assert not square_fits(y-1, angle1, 100, 100)
    (x,y) = square_coords(y, angle1, 100, 100)
    print("Result:", (10000*x+y))

if __name__ == '__main__':
    main()
