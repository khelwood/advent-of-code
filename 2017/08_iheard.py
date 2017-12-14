#!/usr/bin/env python3

import sys
import operator
import re

from collections import defaultdict, namedtuple

Command = namedtuple('Command', 'subject update amount value1 operator value2')

OPS = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
}

LEX_PTN = re.compile(r'^R R R if R\s*([<>=!]+)\s*R\s*$'
    .replace('R',r'(-?\w+)').replace(' ',r'\s+'))

def lex(line):
    m = LEX_PTN.match(line)
    if not m:
        raise ValueError(line)
    return Command(*map(m.group, range(1,7)))

class Registers:
    def __init__(self):
        self._dict = defaultdict(int)
    def __getitem__(self, name):
        if name.startswith('-') or name.isdigit():
            return int(name)
        return self._dict[name]
    def __setitem__(self, name, value):
        self._dict[name] = value
    def values(self):
        return self._dict.values()

def process(registers, line):
    command = lex(line)
    v1 = registers[command.value1]
    v2 = registers[command.value2]
    op = OPS[command.operator]
    if op(v1, v2):
        delta = registers[command.amount]
        if command.update=='dec':
            delta = -delta
        elif command.update!='inc':
            raise ValueError(line)
        x = registers[command.subject] + delta
        registers[command.subject] = x
        return x

def main():
    lines = sys.stdin.read().strip().split('\n')
    registers = Registers()
    greatest = None
    for line in lines:
        v = process(registers, line)
        if v is not None and (greatest is None or greatest < v):
            greatest = v
    print("Max value:", max(registers.values()))
    print("Max ever value:", greatest)

if __name__ == '__main__':
    main()
