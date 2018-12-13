#!/usr/bin/env python3

import sys
import itertools
from collections import defaultdict

def compute_power(serial, x, y):
    rackid = x+10
    power = rackid * (rackid * y + serial)
    return (power//100)%10 - 5

def make_sums(serial, width, height):
    sums = defaultdict(int)
    for (x,y) in itertools.product(
            range(1, width),
            range(1, height)
        ):
        sums[x,y] = (compute_power(serial, x, y) + sums[x, y-1]
                     + sums[x-1, y] - sums[x-1,y-1])
    return sums

def sum_range(sums, x,y, size):
    x0 = x-1
    y0 = y-1
    x1 = x0+size
    y1 = y0+size
    return sums[x1,y1] + sums[x0,y0] - sums[x0,y1] - sums[x1,y0]

def high_spot_3(sums, width, height):
    best_total = -100
    for (x,y) in itertools.product(
            range(1, width-2),
            range(1, height-2)
        ):
        total = sum_range(sums, x, y, 3)
        if total > best_total:
            best_total = total
            best = (x,y)
    return best

def high_spot_any(sums, width, height):
    best_total = -100
    for (x,y) in itertools.product(
            range(1, width),
            range(1, height)
        ):
        ms = 1 + min(width-x, height-y)
        for size in range(1, ms):
            total = sum_range(sums, x, y, size)
            if total > best_total:
                best_total = total
                best = (x,y,size)
    return best

def main():
    WIDTH=301
    HEIGHT=301
    serial = int(sys.argv[1])
    sums = make_sums(serial, WIDTH, HEIGHT)
    x,y = high_spot_3(sums, WIDTH, HEIGHT)
    print(f"High spot for 3 by 3: {x},{y}")
    print("with total:", sum_range(sums, x, y, 3))
    x,y,size = high_spot_any(sums, WIDTH, HEIGHT)
    print(f"High spot for any size: {x},{y},{size}")
    print("with total:", sum_range(sums, x, y, size))

if __name__ == '__main__':
    main()
