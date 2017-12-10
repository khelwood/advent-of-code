#!/usr/bin/env python3

import sys

from hashlib import md5
from point import Point
from collections import namedtuple

PASSCODE = 'lpvhkcbi'

START = Point(0,0)
DEST = Point(3,3)

Door = namedtuple('Door', 'index name direction')
State = namedtuple('State', 'path position')

DOORS = (
    Point( 0,-1),
    Point( 0, 1),
    Point(-1, 0),
    Point( 1, 0),
)

DOORS = tuple(Door(i, *x) for i,x in enumerate(zip('UDLR', DOORS)))
UP, DOWN, LEFT, RIGHT = DOORS

def get_hash(path):
    return md5((PASSCODE+path).encode('ascii')).hexdigest()

def is_open(h, door):
    return ('b' <= h[door.index] <= 'f')

def suggested_doors(pos):
    if pos.x <= pos.y:
        if pos.x < DEST.x:
            yield RIGHT
        if pos.y < DEST.y:
            yield DOWN
        if pos.y > 0:
            yield UP
        if pos.x > 0:
            yield LEFT
    else:
        if pos.y < DEST.y:
            yield DOWN
        if pos.x < DEST.x:
            yield RIGHT
        if pos.x > 0:
            yield LEFT
        if pos.y > 0:
            yield UP

def next_moves(path, pos):
    h = None
    for door in suggested_doors(pos):
        h = h or get_hash(path)
        if is_open(h, door):
            yield door

def find_exit(current_states, next_states):
    for solution in find_exits(current_states, next_states):
        return solution
            
def find_exits(current_states, next_states):
    for state in current_states:
        for door in next_moves(state.path, state.position):
            new_pos = state.position + door.direction
            new_path = state.path + door.name
            if new_pos==DEST:
                yield new_path
            else:
                next_states.append(State(new_path, new_pos))


def main():
    print("Passcode:", PASSCODE)
    current_states = [State('', START)]
    next_states = []
    solution = find_exit(current_states, next_states)
    while not solution:
        current_states = next_states
        next_states = []
        solution = find_exit(current_states, next_states)
    print("Shortest solution:", solution)

    current_states = [State('', START)]
    next_states = []
    while current_states:
        for solution in find_exits(current_states, next_states):
            longest_solution = solution
        current_states = next_states
        next_states = []
    print("Longest solution length:", len(longest_solution))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        PASSCODE = sys.argv[1]
    main()
