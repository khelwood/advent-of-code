#!/usr/bin/env python3

"""
The hallway is a horizontal line of spaces from x=0 to x=10.
Coming down off the hallway are four rooms, at x=2,4,6,8.
Each room is a vertical stack with two spaces.
There are eight pods in four pairs: A, B, C and D.
Two pods start in each room, as described by the puzzle input.
We want to move them so that each pod is in the correct room,
A, B, C, D going left to right.

Each pod can move up,down,left,right into an unoccupied space.
Moving costs energy: A:1, B:10, C:100, D:1000.

Pods never stop on the space immediately outside a room.
Pods never move into a room that is not their correct room.
Pods never move into a room that contains pods of another class.
Once a pod stops moving in a hallway, it will stay there until
it can move into its room.
"""

import sys
import re
from typing import NamedTuple
from collections import defaultdict

ENERGY_COST = (1, 10, 100, 1000)
ROOM_X = (2,4,6,8)
UNSTOPPABLE = set(ROOM_X)
LEVEL = 2

class State(NamedTuple):
    rooms: tuple
    hall : tuple = (None,)*11
    @property
    def solved(self):
        return all(len(room)==LEVEL and all(p==ri for p in room)
                   for ri, room in enumerate(self.rooms))
    def __str__(self):
        rows = [
            [room[LEVEL+ri-len(room)] if len(room)+ri >= LEVEL else None
               for room in self.rooms]
            for ri in range(LEVEL)
        ]
        ordA = ord('A')
        row_lines = ['#'.join(chr(ordA+v) if v is not None else '.' for v in row)
                     for row in rows]

        hall_row = ''.join(chr(ordA+v) if v is not None else '.' for v in self.hall)
        row_lines[0] = '###' + row_lines[0] + '###'
        for i in range(1, len(row_lines)):
            row_lines[i] = '  #' + row_lines[i] + '#'

        return '\n'.join(
            ['#'*13, hall_row] + row_lines + ['  '+'#'*9]
        )

# def make_state(rooms, hall=(None,)*11, real_state=State):
#     for r in rooms:
#         if not isinstance(r, tuple) or not all(isinstance(x, int) for x in r):
#             raise TypeError("Invalid room: "+repr(r))
#     return real_state(rooms, hall)

# State = make_state


def tuple_update(original, pos, new_value):
    return original[:pos] + (new_value,) + original[pos+1:]

def read_input():
    ordA = ord('A')
    rooms = [[] for _ in range(4)]
    for line in sys.stdin.read().strip().splitlines():
        for i,ch in enumerate(re.findall('[A-Z]', line)):
            rooms[i].append(ord(ch)-ordA)
    rooms = tuple(map(tuple, rooms))
    return State(rooms)

def moves(state):
    for i,c in enumerate(state.hall):
        if c is not None:
            e,st = hall_to_room(state, i)
            if st:
                yield e,st
                return
    for rn,room in enumerate(state.rooms):
        if not room:
            continue
        if room[0] != rn or len(room)>1 and any(r!=rn for r in room):
            yield from move_from_room(state, rn)

NO_MOVE = (0, None)

def hall_to_room(state, pos, energy_cost=ENERGY_COST, no_move=NO_MOVE) -> (int, State):
    rooms, hall = state
    pod = hall[pos]
    room = rooms[pod]
    if any(p != pod for p in room):
        return no_move
    target_x = ROOM_X[pod]
    moves = 0
    step = 1 if target_x > pos else -1
    for x in range(pos+step, target_x+step, step):
        if hall[x] is not None:
            return no_move
        moves += 1
    # we are now outside the destination room
    moves += LEVEL-len(room)
    room = (pod,) + room
    hall = tuple_update(hall, pos, None)
    rooms = tuple_update(rooms, pod, room)
    energy = energy_cost[pod] * moves
    return energy, State(rooms, hall)

def room_to_room(state, src, dest, no_move=NO_MOVE, energy_cost=ENERGY_COST):
    rooms, hall = state
    dest_room = rooms[dest]
    if any(d!=dest for d in dest_room):
        return no_move
    moves = 1 + LEVEL - len(rooms[src]) # step out of the room
    step = 1 if dest > src else -1
    for x in range(ROOM_X[src]+step, ROOM_X[dest]+step, step):
        if hall[x] is not None:
            return no_move
        moves += 1
    moves += LEVEL - len(dest_room) # step into the room
    energy = energy_cost[dest]*moves
    dest_room = (dest,) + dest_room
    src_room = rooms[src][1:]
    rooms = tuple(src_room if i==src else dest_room if i==dest
                  else room for (i,room) in enumerate(rooms))
    return energy, State(rooms, hall)


def move_from_room(state, rn, unstoppable=UNSTOPPABLE, energy_cost=ENERGY_COST):
    rooms, hall = state
    room = rooms[rn]
    pod = room[0]
    if pod != rn:
        e, st = room_to_room(state, rn, pod)

        if st:
            yield (e, st)
            return
    start_moves = 1 + LEVEL - len(room) # stepping out of the room
    start_pos = ROOM_X[rn]

    room = room[1:]
    rooms = tuple_update(rooms, rn, room)
    cost = energy_cost[pod]
    moves = start_moves
    for x in range(start_pos-1, -1, -1):
        moves += 1
        if hall[x] is not None:
            break
        if x not in unstoppable:
            new_hall = tuple_update(hall, x, pod)
            yield cost*moves, State(rooms, new_hall)
    moves = start_moves
    for x in range(start_pos+1, len(hall)):
        moves += 1
        if hall[x] is not None:
            break
        if x not in unstoppable:
            new_hall = tuple_update(hall, x, pod)
            yield cost*moves, State(rooms, new_hall)

def solve(initial_state):
    energy_states = defaultdict(set)
    energy_states[0].add(initial_state)
    energy = 0
    seen_states = set()
    while True:
        states = energy_states.get(energy)
        if states:
            print(f"[ energy: {energy} ]", end='\r')
            for state in states:
                if state in seen_states:
                    continue
                seen_states.add(state)
                if state.solved:
                    return energy
                for e,new_state in moves(state):
                    energy_states[energy + e].add(new_state)
        energy += 1
    raise ValueError("Could not solve.")

def level_up(state):
    global LEVEL
    LEVEL = 4
    rooms,hall = state
    inserts = ((3,3), (2,1), (1,0), (0,2))
    rooms = tuple(room[:1] + insert + room[1:]
              for (room, insert) in zip(rooms, inserts))
    return State(rooms, hall)

def main():
    state = read_input()
    e = solve(state)
    print("Part 1 solved with", e, "energy")
    state = level_up(state)
    e = solve(state)
    print("Part 2 solved with", e, "energy")

if __name__ == '__main__':
    main()
