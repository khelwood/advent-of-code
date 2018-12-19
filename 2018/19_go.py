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

def run(ip, commands, registers, cheat=False):
    num_commands = len(commands)
    while 0 <= registers[ip] < num_commands:
        command = commands[registers[ip]]
        command(registers)
        registers[ip] += 1
        if cheat and registers[ip]==1:
            # If we're cheating, then as soon as
            # we get to line 1, we can calculate the answer.
            registers[0] += sum_factors(registers[2])
            break

def sum_factors(num):
    return num + sum(i for i in range(1, num) if num%i==0)

# DIGRESSION: laboriously describe the commands
def explain(ip, commands):
    varnames = list('ABCDEF')
    varnames[ip] = '@'
    varnames = ''.join(varnames)
    num_commands = len(commands)
    for i,command in enumerate(commands):
        print(str(i).rjust(2), explain_command(ip, i, command,
                                                   varnames, num_commands))

def explain_command(ip, i, command, varnames, num_commands):
    op = command.func
    vn = varnames
    a,b,c = command.a, command.b, command.c
    if command.c==ip:
        if op==OpFunc.ADDI:
            if a==ip:
                return f"GOTO {i+b+1}"
            return f"GOTO {vn[a]}+{b+1}"
        if op==OpFunc.ADDR:
            if a==ip or b==ip:
                other = a + b - ip
                return (f"GOTO {vn[other]} + {i+1}"
                        f" // if {vn[other]} GOTO {i+2}")
            return f"GOTO {vn[a]} + {vn[b]} + 1"
        if op==OpFunc.SETI:
            return f"GOTO {a+1}"
        if op==OpFunc.MULR:
            if a==b==ip and i*i+1 >= num_commands:
                return "END"
            return f"GOTO {vn[a]}*{vn[b]} + 1"
    if op==OpFunc.ADDI:
        if a==c:
            return f"{vn[a]} += {b}"
        if a==ip:
            return f"{vn[a]} = {i + b}"
        return f"{vn[a]} = {vn[a]} + {b}"
    if op==OpFunc.ADDR:
        if a==c or b==c:
            other = a+b-c
            if other==ip:
                return f"{vn[c]} += {i}"
            return f"{vn[c]} += {vn[other]}"
        if a==ip or b==ip:
            other = a + b - ip
            return f"{vn[c]} = {vn[other]} + {i}"
        return f"{vn[c]} = {vn[a]} + {vn[b]}"
    if op==OpFunc.SETI:
        return f"{vn[c]} = {a}"
    if op==OpFunc.SETR:
        if a==ip:
            return f"{vn[c]} = {i}"
        return f"{vn[c]} = {vn[a]}"
    if op==OpFunc.MULI:
        if a==c:
            return f"{vn[a]} *= {b}"
        if a==ip:
            return f"{vn[c]} = {i*b}"
        return f"{vn[c]} = {vn[a]} * {b}"
    if op==OpFunc.MULR:
        if a==c or b==c:
            other = a+b-c
            if other==ip:
                return f"{vn[c]} *= {i}"
            return f"{vn[c]} *= {vn[other]}"
        if a==ip or b==ip:
            other = a + b - ip
            return f"{vn[c]} = {vn[other]} * {i}"
        return f"{vn[c]} = {vn[a]} * {vn[b]}"
    if op==OpFunc.EQRR:
        if a==ip or b==ip:
            other = a+b-ip
            return f"{vn[c]} = ({vn[other]}=={i})"
        return f"{vn[c]} = ({vn[a]}=={vn[b]})"
    if op==OpFunc.GTRR:
        if a==ip:
            return f"{vn[c]} = ({i} > {vn[b]})"
        if b==ip:
            return f"{vn[c]} = ({vn[a]} > {i})"
        return f"{vn[c]} = ({vn[a]} > {vn[b]})"
    va = vn[a] if op.areg else a
    vb = vn[b] if op.breg else b
    return f"{vn[c]} = {op.function.__name__}({va}, {vb})"

# As it turns out, this is the program I was given:
#
# 0: goto 17
# 1:
#   registers[0] += sum of factors of registers[2]
#   end program
# 
# 17:
#  if registers[0]:
#    set registers[2] to some value
#    goto 1
#  else
#    set registers[2] to some other value
#    goto 1

def main():
    ip,commands = read_commands()
    #return explain(ip, commands)
    
    registers = [0]*6
    print("Starting with registers[0] =", registers[0])
    run(ip, commands, registers, cheat=True)
    print("Register 0:", registers[0])
    registers = [1] + [0]*5
    print("Starting with registers[0] =", registers[0])
    run(ip, commands, registers, cheat=True)
    print("Register 0:", registers[0])    

if __name__ == '__main__':
    main()
