#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

DanceMove = namedtuple('DanceMove', 'function args')
DanceMove.__call__ = lambda self, programs: self.function(programs, *self.args)

COMMANDS = []

def make_command(expr):
    pattern = re.compile('^' + expr.replace('#', '([0-9a-z]+)') + '$')
    def make_command(function):
        function.pattern = pattern
        COMMANDS.append(function)
        return function
    return make_command

@make_command('s#')
def spin(programs, x):
    x %= len(programs)
    if x==0:
        return programs
    return programs[-x:] + programs[:-x]

@make_command('x#/#')
def exchange(programs, a, b):
    programs[a], programs[b] = programs[b], programs[a]
    return programs

@make_command('p#/#')
def partner(programs, a, b):
    i = programs.index(a)
    j = programs.index(b)
    programs[i], programs[j] = programs[j], programs[i]
    return programs

def parse_move(line):
    for cmd in COMMANDS:
        m = re.match(cmd.pattern, line)
        if m:
            args = tuple(int(x) if x.isdigit() else x for x in m.groups())
            return DanceMove(cmd, args)
    raise ValueError(repr(line))

def read_dance():
    moves = tuple(map(parse_move, sys.stdin.read().split(',')))
    def dance(programs):
        for move in moves:
            programs = move(programs)
        return programs
    return dance

def replay_dance(n, dance, times=1):
    original = [chr(i) for i in range(ord('a'), ord('a')+n)]
    programs = original[:]
    for i in range(times):
        programs = dance(programs)
        if programs==original:
            break
    else:
        return programs
    for _ in range(times%(i+1)):
        programs = dance(programs)
    return programs
        
def main():
    num_programs = int(sys.argv[1]) if len(sys.argv)==2 else 16
    dance = read_dance()
    programs = replay_dance(num_programs, dance)
    print("Result after one dance:", ''.join(programs))
    programs = replay_dance(num_programs, dance, 1_000_000_000)
    print("Result after one billion dances:", ''.join(programs))

if __name__ == '__main__':
    main()
