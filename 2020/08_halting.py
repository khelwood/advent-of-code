#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Instruction = namedtuple('Instruction', 'op arg')

Instruction.__call__ = lambda self, prog: self.op(prog, self.arg)
Instruction.__repr__ = lambda self: f'({self.op.opname}, {self.arg:+d})'

OPERATIONS = {}

def opname(name):
    def opname(func):
        func.opname = name
        OPERATIONS[name] = func
        return func
    return opname

@opname('acc')
def acc(prog, arg):
    prog.acc += arg
    prog.advance()

@opname('jmp')
def jmp(prog, arg):
    prog.position += arg

@opname('nop')
def nop(prog, arg):
    prog.advance()

class Program:
    def __init__(self, instructions):
        self.instructions = instructions
        self.position = 0
        self.acc = 0

    def run_single(self):
        instruction = self.instructions[self.position]
        result = instruction(self)

    def advance(self):
        self.position += 1

def parse_instructions(string):
    return tuple(map(parse_instruction, string.strip().splitlines()))

def parse_instruction(line, ptn=re.compile(r'(\w+)\s+([+-]?\d+)$')):
    m = re.match(ptn, line)
    if not m:
        raise ValueError(line)
    opname = m.group(1)
    op = OPERATIONS[opname]
    arg = int(m.group(2))
    return Instruction(op, arg)

def changes(instructions):
    for i, ins in enumerate(instructions):
        if ins.op==nop:
            changed = list(instructions)
            changed[i] = Instruction(jmp, ins.arg)
            yield changed
        elif ins.op==jmp:
            changed = list(instructions)
            changed[i] = Instruction(nop, ins.arg)
            yield changed

def terminates(prog):
    instructions_run = {}
    pl = len(prog.instructions)
    while 0 <= prog.position < pl:
        v = instructions_run.get(prog.position, 0)
        if v==1:
            return False
        instructions_run[prog.position] = v + 1
        prog.run_single()
    return True

def main():
    instructions = parse_instructions(sys.stdin.read())
    prog = Program(instructions)
    assert not terminates(prog)
    print("Accumulator (infinite loop):", prog.acc)

    for changed in changes(instructions):
        prog = Program(changed)
        if terminates(prog):
            print("Accumulator (terminating):", prog.acc)
            break
    else:
        print("Couldn't fix the program.")

if __name__ == '__main__':
    main()
