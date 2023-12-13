#!/usr/bin/env python3

import sys

from typing import NamedTuple

class Grid(NamedTuple):
    rows: tuple
    columns: tuple

def parse_grid(rows):
    wid = len(rows[0])
    columns = [''.join(row[i] for row in rows) for i in range(wid)]
    return Grid(tuple(rows), tuple(columns))

def iter_blocks(line_iter):
    lines = []
    while True:
        line = next(line_iter, None)
        if line is None:
            break
        line = line.strip()
        if line:
            lines.append(line)
        elif lines:
            yield lines
            lines = []
    if lines:
        yield lines

def differences(a, b):
    c = 0
    for x,y in zip(a,b):
        if x!=y:
            c += 1
    return c

def find_sym(lines):
    n = len(lines)
    for i in range(n-1):
        if (lines[i]==lines[i+1] and
                all(lines[left]==lines[right] for (left, right) in
                    zip(range(i-1, -1, -1), range(i+2, n)))):
            return i+1
    return -1

def close_symmetry_at(lines, i):
    c = differences(lines[i], lines[i+1])
    if c > 1:
        return False
    j = 1
    n = len(lines)
    while i-j >= 0 and i+1+j < n:
        c += differences(lines[i-j], lines[i+1+j])
        if c > 1:
            return False
        j += 1
    return (c==1)

def find_close_sym(lines):
    for i in range(len(lines)-1):
        if close_symmetry_at(lines, i):
            return i+1
    return -1

def find_symmetry(grid, sym_fn):
    x = sym_fn(grid.columns)
    if x >= 0:
        return x
    y = sym_fn(grid.rows)
    if y >= 0:
        return 100*y
    raise ValueError("No symmetry found in grid "+repr(grid))

def main():
    grids = list(map(parse_grid, iter_blocks(sys.stdin)))
    total = sum(find_symmetry(grid, find_sym) for grid in grids)
    print("Part 1:", total)
    total = sum(find_symmetry(grid, find_close_sym) for grid in grids)
    print("Part 2:", total)

if __name__ == '__main__':
    main()
