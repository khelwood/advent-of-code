#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Move = namedtuple('Move', 'value direc next')
State = namedtuple('State', 'name moves')

class Program:
    def __init__(self, start_state, num_steps, states):
        self.start_state = start_state
        self.num_steps = num_steps
        self.states = states
    def run(self):
        ones = set()
        position = 0
        states = self.states
        state = states[self.start_state]
        for i in range(self.num_steps):
            move = state.moves[position in ones]
            if move.value:
                ones.add(position)
            else:
                ones.discard(position)
            position += move.direc
            state = states[move.next]
            if i%100_000==0:
                print('', i, end='\r')
        return len(ones)

def _match(ptn, line, gp=1):
    m = re.match(ptn, line)
    assert m, line
    if gp is not None:
        return m.group(gp)
    return m

def read_program(lines):
    start_state = _match(r'Begin in state (\w+)', lines[0])
    num_steps = int(_match(r'.+after ([0-9]+) steps', lines[1]))
    i = 2
    states = {}
    while i < len(lines):
        i, state = read_state_def(lines, i)
        states[state.name] = state
    return Program(start_state, num_steps, states)

def read_state_def(lines, start):
    name = _match(r'In state (\w+):', lines[start])
    i = start+1
    instructions = [None]*2
    while i < len(lines) and 'current value' in lines[i]:
        i, v, instruction = read_state_instruction(lines, i)
        assert instructions[v] is None
        instructions[v] = instruction
    assert all(instructions)
    return i, State(name, tuple(instructions))

def read_state_instruction(lines, start):
    cur = _match(r'If the current value is ([01])', lines[start])
    new_value = _match(r'- Write the value ([01])', lines[start+1])
    move = _match(r'- Move one slot to the (left|right)', lines[start+2])
    move = 1 if move=='right' else -1
    next_state = _match('- Continue with state (\w+)', lines[start+3])
    return start+4, int(cur), Move(int(new_value), move, next_state)

def main():
    lines = sys.stdin.read().strip().split('\n')
    lines = [line for line in map(str.strip, lines) if line]
    prog = read_program(lines)
    result = prog.run()
    print(("Checksum: %s"%result).ljust(40))

if __name__ == '__main__':
    main()
