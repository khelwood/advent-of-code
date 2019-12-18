#!/usr/bin/env python3

import sys
sys.path.append('..')
from point import Point
from intcode import Program, parse_program_input

SCAFFOLD_S = '#'
OPEN_S = '.'
UP_S = '^'
DOWN_S = 'v'
LEFT_S = '<'
RIGHT_S = '>'
FALLING_S = 'X'

def intersections(lines, char):
    bottom = len(lines)-1
    for y, line in enumerate(lines):
        right = len(line)-1
        for x, ch in enumerate(line):
            if ch!=char:
                continue
            acount = ((x > 0 and line[x-1]==char)
                    + (x < right and line[x+1]==char)
                    + (y > 0 and lines[y-1][x]==char)
                    + (y < bottom and lines[y+1][x]==char))
            if acount >= 3:
                yield (x,y)

def main():
    prog_input = parse_program_input(sys.stdin.read().strip())
    prog = Program(prog_input)
    prog.execute()
    view = prog.output_values
    view = ''.join(map(chr, view)).strip()
    print(view)
    viewlines = view.splitlines()
    alignment = sum(x*y for (x,y) in intersections(viewlines, SCAFFOLD_S))
    print("Alignment:", alignment)


if __name__ == '__main__':
    main()
