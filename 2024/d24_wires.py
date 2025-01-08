#!/usr/bin/env python3

import sys
import re
import operator

from collections import defaultdict
from dataclasses import dataclass
from itertools import chain

OPS = {
    'OR': operator.or_,
    'AND': operator.and_,
    'XOR': operator.xor,
}

OP_ORDER = {op:i for i,op in enumerate((operator.or_, operator.xor, operator.and_))}

OP_STR = {operator.or_:'|', operator.and_:'&', operator.xor:'^'}

def link_op(op):
    return lambda self,other: Link(self, other, op, '')

class Linkable:
    __or__ = link_op(operator.or_)
    __xor__ = link_op(operator.xor)
    __and__ = link_op(operator.and_)

@dataclass
class Value(Linkable):
    value: int
    vo: str

    def canonicalise(self):
        pass

    def __lt__(self, other):
        if isinstance(other, Link):
            return True
        return self.vo < other.vo

    def __call__(self):
        return self.value

    def __repr__(self):
        return self.vo

@dataclass
class Link(Linkable):
    v1: str
    v2: str
    op: callable
    vo: str

    def __call__(self):
        return self.op(self.v1(), self.v2())

    def canonicalise(self):
        self.v1.canonicalise()
        self.v2.canonicalise()
        if self.v2 < self.v1:
            self.v1,self.v2 = self.v2,self.v1

    def __lt__(self, other):
        if isinstance(other, Value):
            return False
        if self.v1 < other.v1:
            return True
        if other.v1 < self.v1:
            return False
        n = OP_ORDER[self.op] - OP_ORDER[other.op]
        if n < 0:
            return True
        if n > 0:
            return False
        return self.v2 < other.v2

    def __repr__(self):
        return f'{self.v1}{OP_STR[self.op]}{self.v2}'


def read_input():
    values = []
    links = []
    ptn = re.compile(r'(\w+)\s*(AND|XOR|OR)\s*(\w+)\s*->\s*(\w+)')
    for line in filter(bool, map(str.strip, sys.stdin)):
        i = line.find(':')
        if i > 0:
            values.append(Value(int(line[i+1:]), line[:i]))
        else:
            m = ptn.fullmatch(line)
            v1,opname,v2,vo = m.groups()
            op = OPS[opname]
            links.append(Link(v1,v2,op,vo))
    return values, links

def nest_links(values, links):
    d = {lk.vo:lk for lk in chain(values, links)}
    for lk in links:
        lk.v1 = d[lk.v1]
        lk.v2 = d[lk.v2]

def create_adder(values):
    x = {int(v.vo[1:]):v for v in values if v.vo.startswith('x')}
    y = {int(v.vo[1:]):v for v in values if v.vo.startswith('y')}
    top = max(x)
    z = {}
    z[0] = x[0]^y[0]
    carry = x[0]&y[0]
    for i in range(1, top + 1):
        xi = x[i]
        yi = y[i]
        x_xor_y = xi^yi
        z[i] = x_xor_y^carry
        carry = (xi&yi) | (x_xor_y & carry)
    z[top+1] = carry
    for k,lk in z.items():
        lk.vo = f'z{k:02d}'
    for lk in z.values():
        lk.canonicalise()
    return {lk.vo:lk for lk in z.values()}

def zvalue(links):
    zd = {lk.vo:lk() for lk in links if lk.vo.startswith('z')}
    z = 0
    for zv in sorted(zd, reverse=True):
        z = (z << 1) | zd[zv]
    return z

def main():
    values, links = read_input()
    nest_links(values, links)
    for link in links:
        link.canonicalise()
    print(zvalue(links))

    links = {lk.vo:lk for lk in links}
    adder = create_adder(values)
    for z in adder.values():
        if repr(links[z.vo]) != repr(z):
            print(z.vo, ':', z)

if __name__ == '__main__':
    main()
