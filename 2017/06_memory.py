#!/usr/bin/env python3

import sys

def redistribute(state):
    state = list(state)
    n = len(state)
    m = max(state)
    i = next(i for i,v in enumerate(state) if v==m)
    state[i] = 0
    while m > 0:
        i = (i+1)%n
        state[i] += 1
        m -= 1
    return tuple(state)

def solve(state):
    cycles = 0
    seen = {state: 0}
    while True:
        state = redistribute(state)
        cycles += 1
        if state in seen:
            break
        seen[state] = cycles
    return cycles, cycles-seen[state]

def main():
    banks = tuple(map(int, sys.stdin.read().split()))
    print(*solve(banks))

if __name__ == '__main__':
    main()
