#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

from opfunc import OpFunc

def setup_command():
    Command = namedtuple('Command', 'func a b c')
    def __call__(self, registers):
        registers[self.c] = self.func(registers, self.a, self.b)
    Command.__call__ = __call__
    return Command

Command = setup_command()

SETIP_PTN = re.compile(r'#ip\s*(\d+)$')
COMMAND_PTN = re.compile(r'(\w+) # # #$'
                        .replace(' ', r'\s+').replace('#', r'(\d+)'))

def read_commands():
    commands = []
    for line in sys.stdin:
        line = line.strip()
        m = re.match(SETIP_PTN, line)
        if m:
            ip = int(m.group(1))
            continue
        m = re.match(COMMAND_PTN, line)
        if not m:
            raise ValueError(repr(line))
        func = OpFunc[m.group(1).upper()]
        command = Command(func, *(int(m.group(i)) for i in (2,3,4)))
        commands.append(command)
    return ip,commands

def run(ip, commands, registers):
    num_commands = len(commands)
    while 0 <= registers[ip] < num_commands:
        command = commands[registers[ip]]
        command(registers)
        registers[ip] += 1

def main():
    ip,commands = read_commands()
    registers = [0]*6
    print("Starting with registers[0] = ", registers[0])
    run(ip, commands, registers)
    print("Register 0:", registers[0])
    registers = [1] + [0]*5
    print("Starting with registers[0] = ", registers[0])
    run(ip, commands, registers)
    print("Register 0:", registers[0])    

if __name__ == '__main__':
    main()
