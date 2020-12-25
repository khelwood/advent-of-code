#!/usr/bin/env python3

import sys

DIVISOR = 20201227

def transform(subject, loops, divisor=DIVISOR):
    value = 1
    for _ in range(loops):
        value *= subject
        value %= divisor
    return value

def findloopsize(publickey, divisor=DIVISOR):
    value = 1
    subject = 7
    loops = 0
    while value != publickey:
        loops += 1
        value = (value*subject)%divisor
    return loops

def main():
    keys = tuple(map(int, sys.argv[1:3]))
    loopsizes = tuple(map(findloopsize, keys))
    print("Loop sizes:", loopsizes)
    print("Encryption key:")
    for key, loopsize in zip(reversed(keys), loopsizes):
        print(transform(key, loopsize))

if __name__ == '__main__':
    main()
