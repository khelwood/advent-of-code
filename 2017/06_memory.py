#!/usr/bin/env python3

import sys

def redistribute(numbers):
    length = len(numbers)
    m = max(numbers)
    pos = next(i for i,x in enumerate(numbers) if x==m)
    numbers[pos] = 0
    while m > 0:
        pos = (pos+1)%length
        numbers[pos] += 1
        m -= 1

def count_till_repeat(numbers):
    steps = 0
    length = len(numbers)
    seen = {tuple(numbers)}
    while len(seen)>steps:
        redistribute(numbers)
        seen.add(tuple(numbers))
        steps += 1
    first_repeat = steps
    numbers_copy = numbers[:]
    cycle = 1
    redistribute(numbers)
    while numbers != numbers_copy:
        cycle += 1
        redistribute(numbers)
    return first_repeat, cycle

def main():
    numbers = [int(n) for n in sys.stdin.read().split()]
    steps, cycle = count_till_repeat(numbers)
    print(steps, cycle)

if __name__ == '__main__':
    main()
