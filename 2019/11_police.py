#!/usr/bin/env python3

import sys

from intcode import Program, parse_program_input

BLACK_N = 0
WHITE_N = 1
LEFT_N = 0
RIGHT_N = 1

def new_direction(old, turn_value):
    x,y = old
    if turn_value==LEFT_N:
        return (y, -x)
    else:
        return (-y, x)

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

class PaintRobot:
    def __init__(self, prog):
        self.prog = prog
        self.panels = {}
        self.pos = (0,0)
        self.direction = (0,-1)
        self.ready_to_move = False
        self.current_colour = BLACK_N
        prog.input_func = self.prog_input
        prog.output_func = self.prog_output
    def prog_input(self):
        return self.current_colour
    def prog_output(self, value):
        if self.ready_to_move:
            self.move(value)
        else:
            self.paint(value)
        self.ready_to_move = not self.ready_to_move
    def paint(self, value):
        self.panels[self.pos] = value
        self.current_colour = value
    def move(self, value):
        self.direction = direc = new_direction(self.direction, value)
        self.pos = pos = addp(self.pos, direc)
        self.current_colour = self.panels.get(pos, BLACK_N)
    def run(self):
        self.prog.execute()

def draw_grid(grid):
    white = {pos for (pos, clr) in grid.items() if clr==WHITE_N}
    x0 = min(x for (x,y) in white)
    y0 = min(y for (x,y) in white)
    x1 = max(x for (x,y) in white) + 1
    y1 = max(y for (x,y) in white) + 1
    for y in range(y0, y1):
        for x in range(x0, x1):
            print('\u2588' if (x,y) in white else ' ', end='')
        print()

def main():
    prog_data = parse_program_input(sys.stdin.read().strip())
    prog = Program(prog_data)
    robot = PaintRobot(prog)
    robot.run()
    print("Number of panels painted:", len(robot.panels))
    prog = Program(prog_data)
    robot = PaintRobot(prog)
    robot.paint(WHITE_N)
    robot.run()
    draw_grid(robot.panels)

if __name__ == '__main__':
    main()
