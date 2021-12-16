#!/usr/bin/env python3

import sys
import math

OPERATORS = (
   sum,
   math.prod,
   min,
   max,
   None,
   lambda seq: int(next(seq) > next(seq)),
   lambda seq: int(next(seq) < next(seq)),
   lambda seq: int(next(seq) == next(seq)),
)

class Packet:
    def __init__(self, version, type_id, value=None, contents=()):
        self.version = version
        self.type_id = type_id
        self.value = value
        self.contents = contents
    def version_sum(self):
        v = self.version
        if self.contents:
            for c in self.contents:
                v += c.version_sum()
        return v
    def evaluate(self):
        if self.value is not None:
            return self.value
        return OPERATORS[self.type_id](p.evaluate() for p in self.contents)

def read_bits():
    h = sys.stdin.read().strip()
    num_bits = len(h)*4
    n = int(h, 16)
    return format(n, f'0{num_bits}b')

def decode_literal(bits, pos):
    more = True
    value = 0
    while more:
        more = (bits[pos] != '0')
        pos += 1
        value = (value << 4) + int(bits[pos:pos+4], 2)
        pos += 4
    return value, pos

def decode_contents(bits, pos):
    ltype = bits[pos]
    pos += 1
    contents = []
    if ltype=='0':
        num_bits = int(bits[pos:pos+15], 2)
        pos += 15
        target = pos + num_bits
        while pos < target:
            p, pos = decode(bits, pos)
            contents.append(p)
    else:
        num_packets = int(bits[pos:pos+11], 2)
        pos += 11
        for _ in range(num_packets):
            p, pos = decode(bits, pos)
            contents.append(p)
    return contents, pos

def decode(bits, pos=0):
    version = int(bits[pos:pos+3], 2)
    pos += 3
    type_id = int(bits[pos:pos+3], 2)
    pos += 3
    if type_id==4:
        value, pos = decode_literal(bits, pos)
        p = Packet(version=version, type_id=type_id, value=value)
    else:
        contents, pos = decode_contents(bits, pos)
        p = Packet(version=version, type_id=type_id, contents=contents)
    return p, pos

def main():
    bits = read_bits()
    root, _ = decode(bits)
    print("Version sum:", root.version_sum())
    print("Value:", root.evaluate())

if __name__ == '__main__':
    main()
