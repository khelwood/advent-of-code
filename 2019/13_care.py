#!/usr/bin/env python3

import sys
import time
from intcode import Program, parse_program_input

EMPTY_N = 0
WALL_N = 1
BLOCK_N = 2
PADDLE_N = 3
BALL_N = 4

NEUTRAL_J = 0
LEFT_J = -1
RIGHT_J = 1

class Game:
    def __init__(self, prog_input, frame_rate=None):
        self.score = 0
        self.screen = {}
        self.joystick = NEUTRAL_J
        self.prog = Program(prog_input)
        self.prog.input_func = self.joy_input
        self.prog.output_func = self.prog_output
        self.ball_x = 0
        self.paddle_x = 0
        self.frame_rate = frame_rate
        self.next_render = 0 if frame_rate else None
    def prog_output(self, value):
        if len(self.prog.output_values)%3==0:
            po = self.prog.output_values
            self.process_output(po[-3],po[-2],po[-1])
    def process_output(self, x,y,value):
        if x==-1 and y==0:
            self.score = value
        self.screen[x,y] = value
        if value==BALL_N:
            self.ball_x = x
        if value==PADDLE_N:
            self.paddle_x = x
    def joy_input(self):
        if self.frame_rate is not None and self.next_render <= time.time():
            self.render()
        bx = self.ball_x
        px = self.paddle_x
        return RIGHT_J if bx > px else LEFT_J if bx < px else NEUTRAL_J
    def play(self):
        self.prog[0] = 2
        self.prog.execute()
    def demo_mode(self):
        self.prog.execute()
    def count_blocks(self):
        return sum(v==BLOCK_N for v in self.screen.values())
    def render(self):
        print(chr(27) + "[2J")
        screen = self.screen
        x0 = min(x for (x,y) in screen if x>=0)
        y0 = min(y for (x,y) in screen if x>=0)
        x1 = max(x for (x,y) in screen) + 1
        y1 = max(y for (x,y) in screen) + 1
        data = '\n'.join([''.join(render_tile(screen.get((x,y), EMPTY_N))
                              for x in range(x0,x1))
                              for y in range(y0,y1)])
        print(data)
        self.next_render = time.time() + self.frame_rate

def render_tile(n):
    if n==EMPTY_N:
        return ' '
    if n==BLOCK_N:
        return '%'
    if n==BALL_N:
        return '*'
    if n==PADDLE_N:
        return '-'
    if n==WALL_N:
        return '\u2588'
    return str(n)


def main():
    prog_input = parse_program_input(sys.stdin.read().strip())
    game = Game(prog_input)
    game.demo_mode()
    num_blocks = game.count_blocks()
    print("Num blocks:", num_blocks)

    game = Game(prog_input)
    game.play()
    print("Game score:", game.score)

if __name__ == '__main__':
    main()
