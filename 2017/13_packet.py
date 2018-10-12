#!/usr/bin/env python3

import sys

class Scanner:
    def __init__(self, depth, ran):
        self.depth = depth
        self.period = 2*ran - 2
        self.severity = depth*ran
    def hits(self, offset):
        return (offset + self.depth)%self.period == 0

def read_scanner(line):
    d,_,r = line.partition(':')
    d,r = (int(x.strip()) for x in (d,r))
    return Scanner(d,r)

def find_offset(scanners):
    offset = 0
    while any(sc.hits(offset) for sc in scanners):
        offset += 1
    return offset

def main():
    scanners = [read_scanner(s) for s in sys.stdin.read().strip().split('\n')]
    severity = sum(sc.severity for sc in scanners if sc.hits(0))
    print("Severity:", severity)
    offset = find_offset(scanners)
    print("Offset:", offset)

if __name__ == '__main__':
    main()
