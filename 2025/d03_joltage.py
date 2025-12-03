#!/usr/bin/env python3

import sys

def joltage(line, digits):
    start = 0
    chars = []
    ll = len(line)
    for dig in reversed(range(digits)):
        start, ch = best_digit(line, start, ll-dig)
        start += 1
        chars.append(ch)
    return int(''.join(chars))

def best_digit(line, start, end):
    besti = -1
    bestch = ''
    for i in range(start, end):
        ch = line[i]
        if ch > bestch:
            bestch = ch
            besti = i
    return besti, bestch

def main():
    lines = sys.stdin.read().strip().splitlines()
    print(sum(joltage(line, 2) for line in lines))
    print(sum(joltage(line, 12) for line in lines))

if __name__ == '__main__':
    main()
