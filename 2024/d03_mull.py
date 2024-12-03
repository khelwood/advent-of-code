#!/usr/bin/env python3

import sys
import re

def summul(txt, ptn=re.compile(r'mul\((-?\d+),(-?\d+)\)')):
    return sum(int(a)*int(b) for a,b in ptn.findall(txt))

def main():
    data = sys.stdin.read().strip()
    print(summul(data))
    enabled = True
    a = 0
    i = data.find('do')
    total = 0
    while i >= 0:
        if enabled and i > a:
            total += summul(data[a:i])
        enabled = not data.startswith("don't", i)
        a = i
        i = data.find('do', i+2)
    if enabled and a < len(data):
        total += summul(data[a:])
    print(total)


if __name__ == '__main__':
    main()
