#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from typing import Optional, Callable
import functools
import operator

OPERATORS = { '+' : operator.add, '*': operator.mul }

@dataclass
class Expression:
    a : Optional[int]
    op : Callable
    b : Optional[int]
    def __call__(self, old):
        a = self.a if self.a is not None else old
        b = self.b if self.b is not None else old
        return self.op(a,b)

@dataclass
class Monkey:
    index: int
    starting_items: tuple
    items = []
    expr: Expression
    test: int
    trueto: int
    falseto: int
    inspection_count=0
    def reset(self):
        self.items = list(self.starting_items)
        self.inspection_count = 0
    def throw(self, monkeys, third=True, limit=None):
        self.inspection_count += len(self.items)
        items = [self.expr(n) for n in self.items]
        new_items = []
        for item in self.items:
            item = self.expr(item)
            if third:
                item //= 3
            elif limit:
                item %= limit
            target = self.falseto if (item % self.test) else self.trueto
            if target==self.index:
                new_items.append(item)
            else:
                monkeys[target].items.append(item)
        self.items = new_items

def parse_monkeys():
    p = re.compile(r'Monkey (\d+):')
    it = iter(sys.stdin.read().splitlines())
    for line in it:
        if (m := p.match(line)):
            yield parse_monkey(int(m.group(1)), it)

def parse_expression(expr, pattern = re.compile(r'new = (\w+) ([*+]) (\w+)')):
    m = pattern.match(expr)
    a = m.group(1)
    op = m.group(2)
    b = m.group(3)
    a = None if a=='old' else int(a)
    b = None if b=='old' else int(b)
    op = OPERATORS[op]
    return Expression(a=a, op=op, b=b)

def parse_monkey(index, lines):
    expression_pattern = re.compile(r'new = (\w+) ([*+]) (\w+)')
    for line in lines:
        line = line.strip()
        if not line:
            break
        if line.startswith('Starting items: '):
            items = tuple(map(int, line[16:].split(', ')))
        elif line.startswith('Operation: '):
            expr = parse_expression(line[11:])
        elif line.startswith('Test: divisible by '):
            n = int(line[19:])
        elif line.startswith('If true: throw to monkey '):
            trueto = int(line[25:])
        elif line.startswith('If false: throw to monkey '):
            falseto = int(line[26:])
        else:
            raise ValueError(line)
    monkey = Monkey(index=index, starting_items=items, expr=expr,
        test=n, trueto=trueto, falseto=falseto)
    monkey.reset()
    return monkey

def main():
    monkeys = list(parse_monkeys())
    for rnd in range(20):
        for monkey in monkeys:
            monkey.throw(monkeys, third=True)
    counts = sorted([monkey.inspection_count for monkey in monkeys], reverse=True)
    print("Part 1 monkey business:", counts[0]*counts[1])
    for monkey in monkeys:
        monkey.reset()
    limit = functools.reduce(operator.mul, (monkey.test for monkey in monkeys))
    for rnd in range(10_000):
        for monkey in monkeys:
            monkey.throw(monkeys, third=False, limit=limit)
    counts = sorted([monkey.inspection_count for monkey in monkeys], reverse=True)
    print("Part 2 monkey business:", counts[0]*counts[1])

if __name__ == '__main__':
    main()
