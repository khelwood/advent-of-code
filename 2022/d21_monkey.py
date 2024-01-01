#!/usr/bin/env python3

import sys
import operator
import z3

from typing import NamedTuple
from collections import defaultdict

OPERATORS = {'+':operator.add, '-':operator.sub,
            '/':operator.truediv, '*':operator.mul}

class Expr(NamedTuple):
    op: callable
    operands: tuple

    def __call__(self, monkeys):
        a,b = self.operands
        return self.op(monkeys[a], monkeys[b])

def parse_monkeys(lines):
    dct = {}
    for line in lines:
        a,b = map(str.strip, line.split(':'))
        if b.isdigit():
            dct[a] = int(b)
        else:
            left,op,right = b.split()
            dct[a] = Expr(OPERATORS[op], (left, right))
    return dct

def resolve(monkeys, links):
    jobs = set()
    seen = set()
    for m,x in monkeys.items():
        if isinstance(x, int):
            seen.add(m)
            for n in links[m]:
                if n not in jobs and all(v in seen for v in monkeys[n].operands):
                    jobs.add(n)
    while jobs:
        old = jobs
        jobs = set()
        for m in old:
            monkeys[m] = monkeys[m](monkeys)
            seen.add(m)
            for n in links[m]:
                if n not in jobs and all(v in seen for v in monkeys[n].operands):
                    jobs.add(n)

def find_root(monkeys):
    links = defaultdict(set)
    for k,x in monkeys.items():
        if isinstance(x, Expr):
            for v in x.operands:
                links[v].add(k)
    resolve(monkeys, links)
    return monkeys['root']

def find_required(monkeys, me):
    var = {m:z3.Int(m) for m in monkeys if m!='root'}
    sol = z3.Solver()
    for m,x in monkeys.items():
        if m==me or m=='root':
            continue
        if isinstance(x, int):
            sol.add(var[m]==x)
        elif x.op==operator.truediv:
            # make sure division is exact even using ints
            a,b = x.operands
            sol.add(var[m]*var[b]==var[a])
        else:
            sol.add(var[m]==x(var))
    a,b = monkeys['root'].operands
    sol.add(var[a]==var[b])
    assert sol.check()==z3.sat
    return sol.model()[var[me]].as_long()

def main():
    lines = sys.stdin.read().strip().splitlines()
    monkeys = parse_monkeys(lines)
    print("Part 1:", int(find_root(monkeys)))
    monkeys = parse_monkeys(lines)
    print("Part 2:", find_required(monkeys, 'humn'))

if __name__ == '__main__':
    main()
