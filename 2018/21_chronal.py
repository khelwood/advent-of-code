#!/usr/bin/env python3

import sys

from opfunc import read_commands, OpFunc

def find_reg_eq(ip, commands, target):
    registers = [0]*6
    num_commands = len(commands)
    while 0 <= registers[ip] < num_commands:
        command = commands[registers[ip]]
        if command.func==OpFunc.EQRR and target in (command.a, command.b):
            other = command.a + command.b - target
            return registers[other]
        if command.func==OpFunc.EQRI and target==command.a:
            return b
        if command.func==OpFunc.EQIR and target==command.b:
            return a
        command(registers)
        registers[ip] += 1

def main():
    ip,commands = read_commands(sys.stdin)
    a = find_reg_eq(ip, commands, 0)
    if a is None:
        print("Couldn't find a good value for register 0.")
        return
    print("Set register 0 to", a)

if __name__ == '__main__':
    main()
