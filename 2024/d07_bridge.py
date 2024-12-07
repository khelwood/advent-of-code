#!/usr/bin/env python3

import sys
import operator
import math
from itertools import product

def parse_line(line):
    a,_,b = line.partition(':')
    return int(a), [int(n) for n in b.split()]

def read_input():
    return list(map(parse_line, filter(bool, map(str.strip, sys.stdin))))

def solvable(target, numbers, ops):
    num_ops = len(numbers)-1
    for comb in product(ops, repeat=num_ops):
        n = numbers[0]
        for i in range(num_ops):
            n = comb[i](n, numbers[i+1])
            if n > target:
                break
        if n==target:
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
