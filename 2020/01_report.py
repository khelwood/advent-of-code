#!/usr/bin/env python3

import sys

def find_2_numbers_with_sum(numbers, target):
    numbers_set = set(numbers)
    for n in numbers:
        if (target-n) in numbers_set:
            return (n, target-n)
    raise ValueError(f"Could not find 2 numbers summing to {target}")

def find_3_numbers_with_sum(numbers, target):
    numbers = sorted(numbers)
    numbers_set = set(numbers)
    for i,a in enumerate(numbers):
        for j in range(i+1, len(numbers)):
            b = numbers[j]
            if a+b >= target:
                break
            if (target - a - b) in numbers_set:
                return (a, b, (target - a - b))
    raise ValueError(f"Could not find 3 numbers summing to {target}")

def main():
    numbers = list(map(int, sys.stdin.read().split()))
    a,b = find_2_numbers_with_sum(numbers, 2020)
    print(f"{a}*{b} == {a*b}")
    a,b,c = find_3_numbers_with_sum(numbers, 2020)
    print(f"{a}*{b}*{c} == {a*b*c}")

if __name__ == '__main__':
    main()
