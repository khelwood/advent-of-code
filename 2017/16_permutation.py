#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

Command = namedtuple('Command', 'pattern function')
Move = namedtuple('Move', 'function arguments')

COMMANDS = []

def make_command(expr):
    pattern = re.compile('^'+expr.replace('#', '([0-9a-z]+)')+'$')
    def command_maker(function):
        cmd = Command(pattern, function)
        COMMANDS.append(cmd)
        return cmd
    return command_maker

@make_command('s#')
def spin(programs, num):
    num = int(num)%len(programs)
    if num:
        programs[:] = programs[-num:] + programs[:-num]

@make_command('x#/#')
def exchange(programs, n1, n2):
    n1,n2 = map(int, (n1, n2))
    programs[n1], programs[n2] = programs[n2], programs[n1]

@make_command('p#/#')
def partner(programs, p1, p2):
    exchange.function(programs, programs.index(p1), programs.index(p2))

def play_dance(programs, moves):
    for move in moves:
        move.function(programs, *move.arguments)

def initialise_programs(n):
    return [chr(ord('a')+i) for i in range(n)]

def replay_dance(programs, moves, times=1):
    original = programs[:]
    for i in range(times):
        play_dance(programs, moves)
        if programs==original:
            break
    else:
        return
    i += 1
    for _ in range(times%i):
        play_dance(programs, moves)

def parse_move(line):
    for cmd in COMMANDS:
        m = re.match(cmd.pattern, line)
        if m:
            return Move(cmd.function, m.groups())
    raise ValueError(repr(line))
        
def main():
    if len(sys.argv) == 2:
        num_programs = int(sys.argv[1])
    else:
        num_programs = 16
    moves = [parse_move(line) for line in sys.stdin.read().strip().split(',')]
    programs = initialise_programs(num_programs)
    play_dance(programs, moves)
    print("Result after one dance:", ''.join(programs))
    programs = initialise_programs(num_programs)
    print(' ...',end='\r')
    replay_dance(programs, moves, 1_000_000_000)
    print("Result after one billion dances:", ''.join(programs))

if __name__ == '__main__':
    main()
