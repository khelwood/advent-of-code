#!/usr/bin/env python3

import sys

def find_repeated(numbers):
    cur = 0
    seen = {0}
    while True:
        for n in numbers:
            cur += n
            if cur in seen:
                return cur
            seen.add(cur)

def main():
    numbers = [int(line) for line in sys.stdin.read().split()]
    print("Resulting frequency:", sum(numbers))
    print("Repeated:", find_repeated(numbers))

if __name__ == '__main__':
    main()
