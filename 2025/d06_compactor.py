#!/usr/bin/env python3

import sys
import operator
from functools import reduce

OPS = {'+':operator.add, '*':operator.mul}

def calculate_grid(rows, ops):
    return sum(reduce(op, (row[i] for row in rows)) for (i,op) in enumerate(ops))

def vertical_parse(lines):
    columns = []
    ll = max(map(len, lines))
    column = []
    for x in reversed(range(ll)):
        chars = []
        for line in lines:
            if len(line) > x and not line[x].isspace():
                chars.append(line[x])
        if chars:
            column.append(int(''.join(chars)))
        elif column:
            columns.append(column)
            column = []
    if column:
        columns.append(column)
    return reversed(columns)

def main():
    lines = sys.stdin.read().rstrip().splitlines()
    ops = [OPS[s] for s in lines.pop(-1).split()]
    nums = [list(map(int, line.split())) for line in lines]
    print(calculate_grid(nums, ops))
    columns = vertical_parse(lines)
    print(sum(reduce(op, col) for (op,col) in zip(ops, columns)))

if __name__ == '__main__':
    main()
