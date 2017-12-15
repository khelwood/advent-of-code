#!/usr/bin/env python3

import sys
import re

from collections import defaultdict

COMMAND_PTN = re.compile(r'([a-z ]+) #,# through #,#'.replace('#','([0-9]+)'))
    
digital_functions = {
    'toggle': lambda v: not v,
    'turn on': lambda v: True,
    'turn off': lambda v: False,
}
analogue_functions = {
    'toggle': lambda v: v+2,
    'turn on': lambda v: v+1,
    'turn off': lambda v: max(0, v-1),
}

def run_command(fn, grid, x0, y0, x1, y1):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            grid[x,y] = fn(grid[x,y])

def process(grid, lines, functions):
    for i,line in enumerate(lines):
        m = COMMAND_PTN.match(line)
        if m is None:
            raise ValueError(repr(line))
        fn = functions[m.group(1)]
        x0, y0, x1, y1 = [int(m.group(i)) for i in range(2, 6)]
        run_command(fn, grid, x0, y0, x1, y1)
        print('',i, end='\r')

def main():
    lines = sys.stdin.read().strip().split('\n')
    grid = defaultdict(bool)
    process(grid, lines, digital_functions)
    on_count = sum(grid.values())
    print("On count:", on_count)
    grid = defaultdict(int)
    process(grid, lines, analogue_functions)
    brightness = sum(grid.values())
    print("Brightness:", brightness)

if __name__ == '__main__':
    main()
