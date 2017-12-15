#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

Scanner = namedtuple('Scanner', 'depth range cycle')

def penalty(scanner):
    if scanner.depth%scanner.cycle==0:
        return scanner.depth*scanner.range
    return 0

def hit(scanner, offset):
    return ((offset+scanner.depth)%scanner.cycle==0)

def make_scanner(line, ptn=re.compile('^([0-9]+):\s*([0-9]+)$')):
    m = ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    d = int(m.group(1))
    r = int(m.group(2))
    c = 2*r - 2
    return Scanner(d, r, c)

def find_offset(scanners):
    offset = 0
    next_print = 0
    while any(hit(sc, offset) for sc in scanners):
        offset += 1
        if offset >= next_print:
            print(' %s  '%offset, end='\r')
            next_print += 100_000
    return offset

def main():
    lines = sys.stdin.read().strip().split('\n')
    scanners = [make_scanner(line) for line in lines]
    severity = sum(map(penalty, scanners))
    print("Severity:", severity)
    offset = find_offset(scanners)
    print("Offset:", offset)

if __name__ == '__main__':
    main()
