#!/usr/bin/env python3

import sys
import operator
import math
from itertools import product

def parse_line(line):
    a,_,b = line.partition(':')
    return int(a), tuple(int(n) for n in b.split())

def read_input():
    return list(map(parse_line, filter(bool, map(str.strip, sys.stdin))))

def solvable(target, numbers, ops):
    if len(numbers)==1:
        return target in numbers
    a = numbers[0]
    b = numbers[1]
    c = numbers[2:]
    for op in ops:
        n = op(a,b)
        if not c:
            if n==target:
                return True
            continue
        if n <= target and solvable(target, (n,)+c, ops):
            return True
    return False


def concat(a,b):
    p = 10 if b==0 else (10**(int(math.log(b, 10))+1))
    return p*a + b

def main():
    equations = read_input()
    ops = (operator.add, operator.mul)
    total = sum(tgt for (tgt, nums) in equations if solvable(tgt, nums, ops))
    print(total)
    ops = (operator.add, operator.mul, concat)
    total = sum(tgt for (tgt, nums) in equations if solvable(tgt, nums, ops))
    print(total)


if __name__ == '__main__':
    main()
