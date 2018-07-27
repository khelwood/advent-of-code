#!/usr/bin/env python3

import sys
import re
import operator

from collections import defaultdict, namedtuple

Command = namedtuple('Command', 'target diff subject op value')

class Program:
    def __init__(self):
        self.registers = defaultdict(int)
        self.max_value = 0
    def __setitem__(self, key, value):
        self.registers[key] = value
        if value > self.max_value:
            self.max_value = value
    def __getitem__(self, key):
        return self.registers[key]

OPERATORS = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '<=': operator.le,
    '>=': operator.ge,
}
    
def read_commands():
    pattern = re.compile(r'@ (inc|dec) # if @ ([!=<>]+) #\s*$'
                             .replace(' ',r'\s+')
                             .replace('@', '([a-z]+)')
                             .replace('#', '(-?[0-9]+)'))
    for line in sys.stdin:
        m = pattern.match(line)
        if not m:
            raise ValueError(repr(line))
        target, incdec, diff, subject, op, value = m.groups()
        diff, value = map(int, (diff, value))
        if incdec=='dec':
            diff = -diff
        yield Command(target, diff, subject, OPERATORS[op], value)

def run(prog, commands):
    for cmd in commands:
        if cmd.op(prog[cmd.subject], cmd.value):
            prog[cmd.target] += cmd.diff
        
def main():
    commands = tuple(read_commands())
    prog = Program()
    run(prog, commands)
    print("Max final value:", max(prog.registers.values()))
    print("Max ever:", prog.max_value)

if __name__ == '__main__':
    main()
