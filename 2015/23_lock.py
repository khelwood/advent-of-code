#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

def isnum(s):
    return s.startswith('-') or s.startswith('+') or s.isdigit()

CommandDef = namedtuple('CommandDef', 'pattern function')
Command = namedtuple('Command', 'function args')

COMMAND_DEFS = []

def def_command(expr):
    ptn = re.compile(expr.replace('#','([a-z0-9+-]+)'))
    def make_command(function):
        cmd = CommandDef(ptn, function)
        COMMAND_DEFS.append(cmd)
        return function
    return make_command

@def_command('inc #')
def inc(prog, name):
    prog[name] += 1

@def_command('hlf #')
def dec(prog, name):
    prog[name] //= 2

@def_command('tpl #')
def tpl(prog, name):
    prog[name] *= 3

@def_command('jmp #')
def jmp(prog, offset):
    prog.next_offset = prog[offset]

@def_command('jie #, #')
def jie(prog, name, offset):
    if prog[name]%2==0:
        prog.next_offset = prog[offset]

@def_command('jio #, #')
def jio(prog, name, offset):
    if prog[name]==1:
        prog.next_offset = prog[offset]

class Program:
    def __init__(self):
        self.registers = {}
        self.next_offset = 1
    def __getitem__(self, name):
        if isnum(name):
            return int(name)
        return self.registers.get(name, 0)
    def __setitem__(self, name, value):
        self.registers[name] = value
    def run(self, commands):
        position = 0
        while 0<=position<len(commands):
            self.next_offset = 1
            cmd = commands[position]
            cmd.function(self, *cmd.args)
            #print(position, cmd.function.__name__, cmd.args, self.registers)
            position += self.next_offset

def parse_command(line):
    for cmddef in COMMAND_DEFS:
        m = re.match(cmddef.pattern, line)
        if m:
            return Command(cmddef.function, m.groups())
    raise ValueError(repr(line))

def main():
    lines = sys.stdin.read().strip().split('\n')
    commands = [parse_command(line) for line in lines]
    prog = Program()
    prog.run(commands)
    print("First run: prog[b]:", prog['b'])
    prog = Program()
    prog['a'] = 1
    prog.run(commands)
    print("Second run: prog[b]:", prog['b'])

if __name__ == '__main__':
    main()
