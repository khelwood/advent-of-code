#!/usr/bin/env python3

import sys
import re

from opfunc import OpFunc

class Case:
    def __init__(self, before, operation, after):
        self.before = before
        self.operation = operation
        self.after = after
    @property
    def opcode(self):
        return self.operation[0]
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
    it = iter(lines)
    cases = [read_case(it) for _ in range((i+1)//4)]
    while not lines[i]:
        i += 1
    program = [tuple(map(int, line.split())) for line in lines[i:]]
    return cases, program

def simple_refine(opfuncs, funcops):
    for op,funcs in enumerate(opfuncs):
        if isinstance(funcs, set) and len(funcs)==1:
            func = next(iter(funcs))
            opfuncs[op] = func
            others = funcops[func]
            if len(others) > 1:
                for other in others:
                    if isinstance(opfuncs[other], set):
                        opfuncs[other].discard(func)
            funcops[func] = op
            return True
    for func, ops in funcops.items():
        if isinstance(ops, set) and len(ops)==1:
            op = next(iter(ops))
            funcops[func] = op
            others = opfuncs[op]
            if len(others) > 1:
                for other in others:
                    if isinstance(funcops[other], set):
                        funcops[other].discard(op)
            opfuncs[op] = func
            return True
    return False

def identify_opcodes(cases, funcs=OpFunc, num_opcodes=16):
    # opfuncs[opcode] = set of possible functions for opcode
    # funcops[func] = set of possible opcodes for function
    opfuncs = [set(funcs) for _ in range(num_opcodes)]
    funcops = { func: set(range(num_opcodes)) for func in funcs }
    for case in cases:
        ofun = opfuncs[case.opcode]
        for func in funcs:
            if not case.matches(func):
                ofun.discard(func)
                funcops[func].discard(case.opcode)
    while simple_refine(opfuncs, funcops):
        pass
    # The input data I got was simple enough that simple_refine
    # identified every opcode. Like a very easy sudoku.
    return opfuncs

def main():
    cases, program = read_input()
    num_3_matches = 0
    for case in cases:
        nm = sum(case.matches(func) for func in OpFunc)
        if nm >= 3:
            num_3_matches += 1
    print("Number of cases matching three or more opcodes:", num_3_matches)
    opfuncs = identify_opcodes(cases)
    registers = [0]*4
    for opcode,a,b,c in program:
        registers[c] = opfuncs[opcode](registers, a, b)
    print("Result of program:", registers[0])

if __name__ == '__main__':
    main()
