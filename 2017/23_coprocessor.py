#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

def isnum(s):
    return s.startswith('-') or s.isdigit()

Command = namedtuple('Command', 'function args')
CommandDef = namedtuple('CommandDef', 'pattern function')
COMMAND_DEFS = []

def def_command(expr):
    pattern = re.compile('^'+expr.replace('#', '(-?[a-z0-9]+)')+'$')
    def def_command(function):
        cdef = CommandDef(pattern, function)
        COMMAND_DEFS.append(cdef)
        return function
    return def_command

@def_command('set # #')
def set_cmd(prog, x, y):
    prog[x] = prog[y]

@def_command('sub # #')
def sub_cmd(prog, x, y):
    prog[x] -= prog[y]

@def_command('mul # #')
def mul_cmd(prog, x, y):
    prog.mul_count += 1
    prog[x] *= prog[y]

@def_command('jnz # #')
def jnz_cmd(prog, x, y):
    if prog[x]:
        return prog[y]

@def_command('jiz # #')
def jiz_cmd(prog, x, y):
    if not prog[x]:
        return prog[y]

def parse_command(line):
    line = line.strip()
    for cdef in COMMAND_DEFS:
        m = cdef.pattern.match(line)
        if m:
            return Command(cdef.function, m.groups())
    raise ValueError(repr(line))

class Program:
    def __init__(self):
        self.registers = {}
        self.mul_count = 0
    def __getitem__(self, name):
        if isnum(name):
            return int(name)
        return self.registers.get(name, 0)
    def __setitem__(self, name, value):
        self.registers[name] = value
    def run(self, commands):
        position = 0
        lc = len(commands)
        while 0 <= position < lc:
            cmd = commands[position]
            r = cmd.function(self, *cmd.args)
            position += 1 if r is None else r

def count_non_primes(start, end, inc):
    sieve = [True]*end
    sieve[0] = sieve[1] = False
    for i in range(4, end, 2):
        sieve[i] = False
    for p in range(3, end, 2):
        if not sieve[p]:
            continue
        for m in range(p+p, end, p):
            sieve[m] = False
    return sum(not sieve[i] for i in range(start, end, inc))

def main():
    lines = sys.stdin.read().strip().split('\n')
    commands = [parse_command(line) for line in lines]
    prog = Program()
    prog.run(commands)
    print("mul count:", prog.mul_count)
    print("I don't know about anyone else's, but my input commands "
              "were counting non-prime numbers in a certain range.")
    for i,cmd in enumerate(commands):
        if cmd.function==jnz_cmd and cmd.args==('a', '2'):
            cmd2 = commands[i+1]
            end = (i+1+int(cmd2.args[-1]))
            break
    for cmd in reversed(commands):
        if cmd.function==sub_cmd and cmd.args[0]=='b':
            inc = -int(cmd.args[1])
            break
    prog = Program()
    prog['a'] = 1
    prog.run(commands[:end])
    start = prog['b']
    end = prog['c']
    if start > end:
        start, end = end, start
    print("start=%s, end=%s, inc=%s"%(start, end, inc))
    result = count_non_primes(start, end+1, abs(inc))
    print(result)

if __name__ == '__main__':
    main()
