#!/usr/bin/env python3

import sys
import re

PTN = re.compile(r'^#-#,\s*#-#\s*$'.replace('#', r'(\d+)'))

def parse_range(line):
    m = re.match(PTN, line)
    return tuple(map(int, m.groups()))

def redundant(items):
    a,b,c,d = items
    return (a <= c <= d <= b) or (c <= a <= b <= d)

def overlaps(items):
    a,b,c,d = items
    return not (b < c or d < a)

def main():
    lines = [parse_range(line) for line in sys.stdin]
    num_redundant = sum(map(redundant, lines))
    print("Num redundant:", num_redundant)
    num_overlaps = sum(map(overlaps, lines))
    print("Num overlaps:", num_overlaps)
    

if __name__ == '__main__':
    main()
