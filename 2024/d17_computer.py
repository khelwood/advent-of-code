#!/usr/bin/env python3

import sys
import re

OPCODES = [None]*8

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

def in_python(a):
    """This is my input, converted into Python code."""
    out = []
    while a:
        b = (a&7)^1
        c = a >> b
        b ^= 5
        b ^= c
        a >>= 3
        out.append(b&7)
    return out

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

def construct_a(pieces):
    a = 0
    for p in pieces:
        a = 8*a + p
    return a

def find_pieces(codes, pieces, index=0):
    outdex = len(codes)-1-index
    for n in range(8):
        pieces[index] = n
        out = in_python(construct_a(pieces))
        if len(out)==len(codes) and out[outdex]==codes[outdex]:
            if outdex==0:
                return pieces
            r = find_pieces(codes, pieces, index+1)
            if r:
                return r
    return None

def main():
    regs, codes = read_input()
    m = Machine(*regs)
    out = m.run(codes)
    print(','.join(map(str, out)))
    pieces = [1]*len(codes)
    r = find_pieces(codes, pieces)
    print(construct_a(r))

if __name__ == '__main__':
    main()
