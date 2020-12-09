#!/usr/bin/env python3

import sys
from itertools import islice

def read_numbers():
    return tuple(map(int, sys.stdin))

def enum_slice(items, start, end):
    return enumerate(islice(items, start, end), start)

def find_sum_two(numbers, start, end, target):
    for i, a in enum_slice(numbers, start, end):
        for b in islice(numbers, i+1, end):
            if a+b == target:
                return (a,b)
    return None

def find_contiguous_sum(numbers, target):
    i = 0
    running_sum = numbers[0]
    for j,n in enum_slice(numbers, 1, None):
        running_sum += n
        while running_sum > target and i < j-1:
            running_sum -= numbers[i]
            i += 1
        if running_sum==target:
            return (i,j)

def find_encryption_weakness(numbers, i, j):
    n0 = min(islice(numbers, i, j+1))
    n1 = max(islice(numbers, i, j+1))
    return n0 + n1

def main():
    chunk = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    numbers = read_numbers()
    for i,n in enum_slice(numbers, chunk, None):
        if not find_sum_two(numbers, i - chunk, i, n):
            wrong_number = n
            break
    print("Invalid number:", wrong_number)
    i,j = find_contiguous_sum(numbers, wrong_number)
    print(f"Contiguous block: {i} ({numbers[i]}) to {j} ({numbers[j]}).")
    print("Encryption weakness:", find_encryption_weakness(numbers, i, j))

if __name__ == '__main__':
    main()
