#!/usr/bin/env python3

import sys
from string import ascii_lowercase, ascii_uppercase

PRIORITY = dict(zip(ascii_lowercase + ascii_uppercase, range(1, 53)))

def common(string):
    n = len(string)//2
    c, = set(string[:n]) & set(string[n:])
    return c

def groups(lines):
    return (lines[i:i+3] for i in range(0, len(lines), 3))

def group_common(lines):
    a,b,c = lines
    v, = set(a) & set(b) & set(c)
    return v

def main():
    data = list(filter(bool, map(str.strip, sys.stdin)))
    total_priority = sum(PRIORITY[common(line)] for line in data)
    print("Total priority:", total_priority)
    total_priority = sum(PRIORITY[group_common(gp)] for gp in groups(data))
    print("Total priority:", total_priority)

if __name__ == '__main__':
    main()
