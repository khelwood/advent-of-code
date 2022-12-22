#!/usr/bin/env python3

import sys

def read_ops():
    for line in sys.stdin.read().splitlines():
        if line=='noop':
            yield None
        else:
            yield int(line[5:])

def run_ops(ops):
    cycle = 0
    value = 1
    strength = 0
    for op in ops:
        cycle += 1
        if cycle%40==20:
            strength += cycle * value
        if op is not None:
            cycle += 1
            if cycle%40==20:
                strength += cycle * value
            value += op
    return strength

def find_pixels(ops, w=40):
    cycle = 0
    value = 1
    pixels = set()
    for op in ops:
        y,x = divmod(cycle, w)
        cycle += 1
        if abs(x-value) <= 1:
            pixels.add((x,y))
        if op is not None:
            y,x = divmod(cycle, w)
            cycle += 1
            if abs(x-value) <= 1:
                pixels.add((x,y))
            value += op
    return pixels

def render(pixels, w=40, h=6):
    xr = range(w)
    for y in range(h):
        print()
        for x in xr:
            print('#' if (x,y) in pixels else ' ', end='')
    print()

def main():
    ops = list(read_ops())
    print("Strength:", run_ops(ops))
    pixels = find_pixels(ops)
    render(pixels)

if __name__ == '__main__':
    main()
