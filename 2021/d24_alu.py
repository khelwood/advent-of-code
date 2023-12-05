#!/usr/bin/env python3

"""
IDEA TO SOLVE:
The validation for 99 999 999 997 and 99 999 999 996 are the same
until the last digit; so cache the state after validating the first N digits.
"""

import sys
from typing import NamedTuple
from types import FunctionType

COMMANDS = {}

def command(pattern):
    words = pattern.split()
    num_args = len(words)-1
    name = words[0]
    def command(func):
        func.num_args = num_args
        COMMANDS[name] = func
        return func
    return command

class CommandLine(NamedTuple):
    func: FunctionType
    args: tuple

    def __call__(self, alu):
        self.func(alu, *self.args)
    def __str__(self):
        return f'{self.func.__name__}{self.args}'

class Alu:
    def __init__(self, commands):
        self.commands = commands
        self.data = None
    def run(self, data):
        self.data = data
        self.data_pos = 0
        self.line_pos = 0
        self.var = dict.fromkeys('xyzw', 0)
        for com in self.commands:
            #print("Executing", com)
            com(self)
            #print(self.var)
    def read(self):
        value = self.data[self.data_pos]
        self.data_pos += 1
        return value
    def __setitem__(self, name, value):
        self.var[name] = value
    def __getitem__(self, name):
        if isinstance(name, int):
            return name
        return self.var[name]

@command('inp @')
def inp(alu, name):
    alu[name] = alu.read()

@command('add @ @')
def add(alu, a, b):
    alu[a] = alu[a] + alu[b]

@command('mul @ @')
def mul(alu, a, b):
    alu[a] = alu[a] * alu[b]

@command('div @ @')
def div(alu, a, b):
    n = alu[a]
    d = alu[b]
    if (n < 0) != (d < 0):
        alu[a] = -(abs(n)//abs(d))
    else:
        alu[a] = n//d

@command('mod @ @')
def mod(alu, a, b):
    alu[a] = alu[a] % alu[b]

@command('eql @ @')
def eql(alu, a, b):
    alu[a] = int(alu[a]==alu[b])

def intify(string):
    try:
        return int(string)
    except ValueError:
        return string

def parse_command(line):
    funcname, *args = line.split()
    func = COMMANDS[funcname]
    assert func.num_args==len(args)
    args = tuple(intify(w) for w in args)
    return CommandLine(func, args)

def iter_candidates():
    num = 10**14
    while True:
        num -= 1
        data = tuple(int(d) for d in str(num))
        if 0 not in data:
            yield data

def find_valid(alu, candidates):
    for data in candidates:
        alu.run(data)
        if alu['z']==0:
            return data
        print(f' {data}', end='\r')

def main():
    commands = tuple(map(parse_command, sys.stdin.read().strip().splitlines()))
    alu = Alu(commands)
    data = find_valid(alu, iter_candidates())
    print("Valid number:", ''.join(map(str, data)))

if __name__ == '__main__':
    main()
