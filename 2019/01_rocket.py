#!/usr/bin/env python3

import sys

def mass_fuel(mass):
    return max(mass//3 - 2, 0)

def rec_fuel(mass):
    total = 0
    f = mass_fuel(mass)
    while f > 0:
        total += f
        f = mass_fuel(f)
    return total

def main():
    masses = list(map(int, sys.stdin.read().split()))
    print("Part one:", sum(map(mass_fuel, masses)))
    print("Part two:", sum(map(rec_fuel, masses)))

if __name__ == '__main__':
    main()
