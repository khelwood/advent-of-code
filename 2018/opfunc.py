#!/usr/bin/env python3

import operator
import re
from enum import Enum
from collections import namedtuple

def first(a,b=None):
    return a

class OpFunc(Enum):
    ADDR = (operator.add, True, True)
    ADDI = (operator.add, True, False)
    MULR = (operator.mul, True, True)
    MULI = (operator.mul, True, False)
    BANR = (operator.and_, True, True)
    BANI = (operator.and_, True, False)
    BORR = (operator.or_, True, True)
    BORI = (operator.or_, True, False)
    SETR = (first, True, None)
    SETI = (first, False, None)
    GTIR = (operator.gt, False, True)
    GTRI = (operator.gt, True, False)
    GTRR = (operator.gt, True, True)
    EQIR = (operator.eq, False, True)
    EQRI = (operator.eq, True, False)
    EQRR = (operator.eq, True, True)
    @property
    def function(self):
        return self.value[0]
    @property
    def areg(self):
        return self.value[1]
    @property
    def breg(self):
        return self.value[2]
    def __repr__(self):
        return 'OpFunc.'+self.name
    def __call__(self, registers, a, b):
        if self.areg:
            a = registers[a]
        if self.breg:
            b = registers[b]
        return self.function(a,b)

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

def read_commands(lines):
    commands = []
    for line in lines:
        line = line.strip()
        m = re.match(SETIP_PTN, line)
        if m:
            ip = int(m.group(1))
            continue
        line, _, _ = line.partition('#') # I added some comments - omit them
        line = line.strip()
        m = re.match(COMMAND_PTN, line)
        if not m:
            raise ValueError(repr(line))
        func = OpFunc[m.group(1).upper()]
        command = Command(func, *(int(m.group(i)) for i in (2,3,4)))
        commands.append(command)
    return ip,commands


# DIGRESSION: laboriously describe the commands
def explain(ip, commands):
    varnames = list('ABCDEF')
    varnames[ip] = '@'
    varnames = ''.join(varnames)
    num_commands = len(commands)
    print("    #ip",ip)
    for i,command in enumerate(commands):
        print(str(i).rjust(2), ' ', explain_command(ip, i, command,
                                                   varnames, num_commands))

def explain_command(ip, i, command, varnames, num_commands=None):
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
                        f" // if {vn[other]} SKIP")
            return f"GOTO {vn[a]} + {vn[b]} + 1"
        if op==OpFunc.SETI:
            return f"GOTO {a+1}"
        if op==OpFunc.MULR:
            if num_commands is not None and a==b==ip and i*i+1 >= num_commands:
                return "END"
            return f"GOTO {vn[a]}*{vn[b]} + 1"
    if op==OpFunc.ADDI:
        if a==c:
            return f"{vn[c]} += {b}"
        if a==ip:
            return f"{vn[c]} = {i + b}"
        return f"{vn[c]} = {vn[a]} + {b}"
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
    if op==OpFunc.EQRI:
        return f"{vn[c]} = ({vn[a]}=={b})"
    if op==OpFunc.GTRR:
        if a==ip:
            return f"{vn[c]} = ({i} > {vn[b]})"
        if b==ip:
            return f"{vn[c]} = ({vn[a]} > {i})"
        return f"{vn[c]} = ({vn[a]} > {vn[b]})"
    if op==OpFunc.GTIR:
        return f"{vn[c]} = ({a} > {vn[b]})"
    if op==OpFunc.BANI:
        if a==c:
            return f"{vn[c]} &= {b}"
        return f"{vn[c]} = {vn[a]} & {b}"
    if op==OpFunc.BORI:
        if a==c:
            return f"{vn[c]} |= {b}"
        return f"{vn[c]} = {vn[a]} | {b}"
    va = vn[a] if op.areg else a
    vb = vn[b] if op.breg else b
    return f"{vn[c]} = {op.function.__name__}({va}, {vb})"

def main():
    import sys
    ip, commands = read_commands(sys.stdin)
    explain(ip, commands)

if __name__=='__main__':
    main()
