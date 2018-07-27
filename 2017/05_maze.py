#!/usr/bin/env python3

import sys

def follow(data, update):
    data = list(data)
    n = len(data)
    i = 0
    jumps = 0
    while 0 <= i < n:
        d = data[i]
        data[i] += update(d)
        i += d
        jumps += 1
    return jumps
        
def main():
    data = tuple(map(int, sys.stdin))
    print(follow(data, lambda n: 1))
    print(follow(data, lambda n: 1 if n<3 else -1))

if __name__ == '__main__':
    main()
