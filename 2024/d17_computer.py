#!/usr/bin/env python3

import sys
import re
import time

OPCODES = {}

def opcode(n):
    def decorator(f):
        OPCODES[n] = f
        return f
    return decorator

class Machine:
    def __init__(self, a, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
        self.output = []

    def operand(self, n):
        match n:
            case 4: return self.a
            case 5: return self.b
            case 6: return self.c
        return n

    def dv(self, n):
        return self.a >> self.operand(n)

    @opcode(0)
    def adv(self, n):
        self.a = self.dv(n)

    @opcode(1)
    def bxl(self, n):
        self.b ^= n

    @opcode(2)
    def bst(self, n):
        self.b = (self.operand(n)&7)

    @opcode(3)
    def jnz(self, n):
        if self.a:
            return n

    @opcode(4)
    def bxc(self, _):
        self.b ^= self.c

    @opcode(5)
    def out(self, n):
        self.output.append(self.operand(n)&7)

    @opcode(6)
    def bdv(self, n):
        self.b = self.dv(n)

    @opcode(7)
    def cdv(self, n):
        self.c = self.dv(n)

    def run(self, codes):
        pos = 0
        nc = len(codes)
        while 0 <= pos < nc:
            fi = codes[pos]
            vi = codes[pos+1]
            r = OPCODES[fi](self, vi)
            if r is None:
                pos += 2
            else:
                pos = r
        return self.output

def as_python(a):
    """This is my input, converted into Python code."""
    while a:
        b = (a&7)^1
        c = a >> b
        b ^= 5
        b ^= c
        a >>= 3
        yield (b&7)

def read_input():
    rpn = re.compile(r'^Register (\w): (\d+)$')
    ppn = re.compile(r'^Program: ([0-9,]+)$')
    regs = [None]*3
    for line in sys.stdin:
        if (m := rpn.match(line)):
            r = ord(m.group(1))-ord('A')
            v = int(m.group(2))
            regs[r] = v
        elif (m := ppn.match(line)):
            v = m.group(1)
            codes = list(map(int, v.split(',')))
    return regs, codes

def test_a(codes, a):
    n = 0
    nc = len(codes)
    for v in as_python(a):
        if n >= nc or v != codes[n]:
            return False
        n += 1
    return (n==nc)

def main():
    regs, codes = read_input()
    m = Machine(*regs)
    out = m.run(codes)
    print(','.join(map(str, out)))
    lower = 1<<(3*(len(codes)-1))
    upper = 1<<(3*len(codes))
    for a in range(lower, upper):
        if test_a(codes, a):
            print(a)
            break

if __name__ == '__main__':
    main()
