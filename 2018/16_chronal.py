#!/usr/bin/env python3

import sys
import re
import operator
from collections import namedtuple

def first(a,b=None):
    return a

OpFunc = namedtuple('OpFunc', 'func areg breg')

OPFUNCS = ((operator.add, True, True),
            (operator.add, True, False),
            (operator.mul, True, True),
            (operator.mul, True, False),
            (operator.and_, True, True),
            (operator.and_, True, False),
            (operator.or_, True, True),
            (operator.or_, True, False),
            (first, True, None),
            (first, False, None),
            (operator.gt, False, True),
            (operator.gt, True, False),
            (operator.gt, True, True),
            (operator.eq, False, True),
            (operator.eq, True, False),
            (operator.eq, True, True),
        )

OPFUNCS = tuple(OpFunc(*args) for args in OPFUNCS)

def __call__(self, registers, a, b):
    if self.areg:
        a = registers[a]
    if self.breg:
        b = registers[b]
    return self.func(a,b)

OpFunc.__call__ = __call__
del __call__
    
class Case:
    def __init__(self, before, operation, after):
        self.before = before
        self.operation = operation
        self.after = after
    def matches(self, opfunc):
        op,a,b,c = self.operation
        return (self.after[c]==opfunc(self.before, a, b))
    def __str__(self):
        return (f"Before: {self.before}\n{' '.join(map(str, self.operation))}"
             f"\nAfter: {self.after}")

REGISTERS_PTN = re.compile(r'\[ # , # , # , # \]'.replace('#', r'(\d+)')
                               .replace(' ', r'\s*'))
    
def read_case(line_iter, rptn=REGISTERS_PTN):
    line = next(line_iter, None)
    if line=='':
        line = next(line_iter, None)
    if line is None:
        return None
    m = rptn.search(line)
    if not m:
        raise ValueError(repr(line))
    bef = tuple(map(int, m.groups()))
    op = tuple(map(int, next(line_iter).split()))
    m = rptn.search(next(line_iter))
    if not m:
        raise ValueError(repr(line))
    aft = tuple(map(int, m.groups()))
    return Case(bef, op, aft)

def read_input():
    lines = [line.strip() for line in sys.stdin]
    i = len(lines)-1
    while not lines[i].startswith("After:"):
        i -= 1
    i += 1
    test_case_lines = lines[:i]
    it = iter(lines)
    return [read_case(it) for _ in range((i+1)//4)]

def main():
    cases = read_input()
    num_3_matches = 0
    print("Number of cases:", len(cases))
    for case in cases:
        nm = sum(case.matches(func) for func in OPFUNCS)
        if nm >= 3:
            num_3_matches += 1
    print("Number of cases matching three or more opcodes:", num_3_matches)

if __name__ == '__main__':
    main()
