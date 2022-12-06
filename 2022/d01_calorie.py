#!/usr/bin/env python3

import sys

def read_input():
    current = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            if current:
                yield current
                current = []
        else:
            current.append(int(line))
    if current:
        yield current

def main():
    elfs = list(read_input())
    sums = list(map(sum, elfs))
    max_elf = max(sums)
    print("Max elf:", max_elf)
    sums.sort(reverse=True)
    print("Total of top three elfs:", sum(sums[:3]))


if __name__ == '__main__':
    main()
