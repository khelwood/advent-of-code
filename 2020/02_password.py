#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Entry = namedtuple('Entry', 'num1 num2 char string')

def check_one(entry):
    return entry.num1 <= entry.string.count(entry.char) <= entry.num2

def check_two(entry):
    return ((entry.string[entry.num1-1]==entry.char)
            ^(entry.string[entry.num2-1]==entry.char))

LINE_PATTERN = re.compile(r'^(\d+)-(\d+) (\w): (\w+)$')
    
def parse(line):
    m = LINE_PATTERN.match(line)
    return Entry(int(m.group(1)), int(m.group(2)),
                     m.group(3), m.group(4))

def main():
    entries = [parse(line) for line in sys.stdin.read().splitlines()]
    one_count = sum(map(check_one, entries))
    print("Part one:", one_count)
    two_count = sum(map(check_two, entries))
    print("Part two:", two_count)

if __name__ == '__main__':
    main()
