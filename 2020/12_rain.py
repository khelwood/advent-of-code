#!/usr/bin/env python3

import sys
from collections import namedtuple

NORTH = (0,-1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

OPERATIONS = {}

def opname(name):
    def operation(func):
        func.opname = name
        OPERATIONS[name] = func
        return func
    return operation

for ch, direc in zip('NESW', (NORTH, EAST, SOUTH, WEST)):
    @opname(ch)
    def move(ship, distance, direc=direc):
        ship.move(direc, distance)
    del move

@opname('L')
def left(ship, angle):
    ship.turn_left(angle)

@opname('R')
def right(ship, angle):
    ship.turn_left(-angle)

@opname('F')
def forwards(ship, distance):
    ship.forwards(distance)

def rotate(p, angle):
    turns = (angle // 90) % 4
    if turns==0:
        return p
    x,y = p
    if turns==1:
        return (y, -x)
    if turns==2:
        return (-x, -y)
    if turns==3:
        return (-y, x)
    raise ValueError("weird angle: %r"%angle)


class Ship:
    def __init__(self):
        self.orientation = EAST
        self.position = (0,0)
    def turn_left(self, angle):
        self.orientation = rotate(self.orientation, angle)
    def translate(self, direc, distance):
        rx, ry = direc
        x, y = self.position
        self.position = (x + rx*distance, y + ry*distance)
    move = translate
    def forwards(self, distance):
        self.translate(self.orientation, distance)
    def __repr__(self):
        return f"Ship(orientation={self.orientation}, position={self.position})"

class Wayship(Ship):
    def move(self, direc, distance):
        x,y = self.orientation
        rx, ry = direc
        self.orientation = (x + rx*distance, y + ry*distance)


Instruction = namedtuple('Instruction', 'function argument')
Instruction.__call__ = lambda self, ship: self.function(ship, self.argument)

def parse_instruction(line):
    return Instruction(OPERATIONS[line[0]], int(line[1:]))

def main():
    instructions = tuple(map(parse_instruction, sys.stdin))
    ship = Ship()
    for instruction in instructions:
        instruction(ship)
    print(ship)
    print("Manhattan distance:", sum(map(abs, ship.position)))
    ship = Wayship()
    ship.orientation = (10, -1)
    for instruction in instructions:
        instruction(ship)
    print(ship)
    print("Manhattan distance:", sum(map(abs, ship.position)))


if __name__ == '__main__':
    main()
