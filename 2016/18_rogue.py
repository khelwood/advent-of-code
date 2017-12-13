#!/usr/bin/env python3

import sys

TRAP = '^'
SAFE = '.'

def traps(prev_row):
    return ''.join(trap_content(prev_row, i) for i in range(len(prev_row)))

def get_def(seq, index, default=None):
    if 0<=index<len(seq):
        return seq[index]
    return default

def trap_content(prev_row, i):
    if get_def(prev_row, i-1, SAFE)==get_def(prev_row, i+1, SAFE):
        return SAFE
    return TRAP

# The rows don't repeat with 400000, so we can't even
#  find a cycle and multiply it up.
def count_safe(first, num_rows):
    row = first
    result = row.count(SAFE)
    next_print = 0
    for i in range(num_rows-1):
        if i>=next_print:
            print(" %r   "%i, end='\r')
            next_print += 4000
        row = traps(row)
        result += row.count(SAFE)
    return result

def main():
    data = sys.stdin.read().strip()
    num_rowses = [40, 400000]
    for num_rows in num_rowses:
        print("\nNum rows:", num_rows)
        num_safe = count_safe(data, num_rows)
        print("Num safe:", num_safe)

if __name__ == '__main__':
    main()
