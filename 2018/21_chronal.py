#!/usr/bin/env python3

import sys

from opfunc import read_commands

EMIT = object()

def emit_targets(ip, commands):
    registers = [0]*6
    targets = set()
    num_commands = len(commands)
    while 0 <= registers[ip] < num_commands:
        command = commands[registers[ip]]
        if command is EMIT:
            target = registers[5]
            if target in targets:
                return
            yield target
            targets.add(target)
            registers[2] = 0
        else:
            command(registers)
        registers[ip] += 1

def shortcut(registers):
    registers[2] = registers[4] // 256
    registers[1] = 25

def simplify(commands):
    commands[17] = shortcut
    for i in range(18,26):
        commands[i] = None
    commands[28] = EMIT

def main():
    ip,commands = read_commands(sys.stdin)
    simplify(commands)
    program = emit_targets(ip, commands)
    a = next(program)
    print("First halting value:", a)
    for a in program:
        #print(a, end=',')
        pass
    print("Last halting value:", a)

if __name__ == '__main__':
    main()
