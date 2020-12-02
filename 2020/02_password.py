#!/usr/bin/env python3

import sys
import re

class Entry:
    def __init__(self, num1, num2, char, string):
        self.num1 = num1
        self.num2 = num2
        self.char = char
        self.string = string
    @property
    def alpha(self):
        return self.num1 <= self.string.count(self.char) <= self.num2
    @property
    def beta(self):
        return ((self.string[self.num1-1]==self.char)
                    ^(self.string[self.num2-1]==self.char))

LINE_PATTERN = re.compile('^(#)-(#) (C): (C+)$'.replace('#', r'\d+')
                              .replace('C', r'\w'))
    
def parse(line):
    m = LINE_PATTERN.match(line)
    return Entry(int(m.group(1)), int(m.group(2)),
                     m.group(3), m.group(4))

def main():
    entries = [parse(line) for line in sys.stdin.read().splitlines()]
    one_count = sum(entry.alpha for entry in entries)
    print("Part one:", one_count)
    two_count = sum(entry.beta for entry in entries)
    print("Part two:", two_count)

if __name__ == '__main__':
    main()
