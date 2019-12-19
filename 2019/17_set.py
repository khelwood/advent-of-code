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
            if (char==char and x>0 and x < right and y > 0 and y < bottom
                  and line[x-1]==char and line[x+1]==char
                  and lines[y-1][x]==char and lines[y+1][x]==char):
                yield Point(x,y)

class LineGrid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = self.height and len(lines[0])
        self.lines = lines
    def __getitem__(self, index):
        x,y = index
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.lines[y][x]
    def find(self, char):
        for y,line in enumerate(self.lines):
            if char in line:
                return Point(line.index(char), y)
        return None

def find_path(grid):
    pos = grid.find('^')
    turn = 'L'
    direc = Point(-1,0)
    while True:
        steps = 0
        nextpos = pos + direc
        while grid[nextpos]==SCAFFOLD_S:
            pos = nextpos
            nextpos = pos + direc
            steps += 1
        yield turn, steps
        turn = 'L'
        direc = Point(direc.y, -direc.x)
        if grid[pos + direc] != SCAFFOLD_S:
            turn = 'R'
            direc = -direc
            if grid[pos + direc] != SCAFFOLD_S:
                break

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
    grid = LineGrid(viewlines)
    print("Route:")
    print(','.join(t+str(s) for (t,s) in find_path(grid)))
    # I didn't find this programmatically, just from inspection
    patternA = 'L,12,L,12,R,12'
    patternB = 'L,8,L,8,R,12,L,8,L,8'
    patternC = 'L,10,R,8,R,12'
    route = 'A,A,B,C,C,A,B,C,A,B'
    feed = 'n\n'
    input_string = '\n'.join([route, patternA, patternB, patternC, feed])
    prog_data = list(prog_input)
    prog_data[0] = 2
    prog = Program(prog_data)
    prog.run_input(input_string)
    print(''.join(chr(v) if v < 256 else '\n%s'%v for v in prog.output_values))


if __name__ == '__main__':
    main()
