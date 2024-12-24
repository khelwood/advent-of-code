#!/usr/bin/env python3

import sys
import re
import operator

from collections import defaultdict
from typing import NamedTuple

OPS = {
    'OR': operator.or_,
    'AND': operator.and_,
    'XOR': operator.xor,
}

class Value(NamedTuple):
    value: int
    vo: str

class Link(NamedTuple):
    v1: str
    v2: str
    op: callable
    vo: str

    def __call__(self, vars):
        v1 = vars[self.v1]
        v2 = vars[self.v2]
        return self.op(v1,v2)


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

def dependencies(values, links):
    known = {v.vo for v in values}
    precedes = defaultdict(set)
    follows = defaultdict(set)
    for link in links:
        f = follows[link.vo]
        if link.v1 not in known:
            f.add(link.v1)
            precedes[link.v1].add(link.vo)
        if link.v2 not in known:
            f.add(link.v2)
            precedes[link.v2].add(link.vo)
    return precedes, follows

def topsort(precedes, follows, links):
    output = []
    new = [x for x in precedes if not follows[x]]
    done = set()
    while new:
        done.update(new)
        cur = new
        new = set()
        for nv in cur:
            output.append(nv)
            for f in precedes[nv]:
                nvf = follows[f]
                nvf.remove(nv)
                if not nvf:
                    new.add(f)
            del precedes[nv]
    for link in links:
        if link.vo not in done:
            output.append(link.vo)
    return output

def resolve_values(values, links, link_order):
    d = {v.vo:v.value for v in values}
    link_dict = {lk.vo : lk for lk in links}
    for vo in link_order:
        lk = link_dict.get(vo)
        if lk:
            d[vo] = lk(d)
    return d

def zvalue(d):
    zd = {k:v for k,v in d.items() if k.startswith('z')}
    z = 0
    for zv in sorted(zd, reverse=True):
        z = (z << 1) | zd[zv]
    return z

def main():
    values, links = read_input()
    precedes, follows = dependencies(values, links)

    link_order = topsort(precedes, follows, links)
    value_dict = resolve_values(values, links, link_order)
    print(zvalue(value_dict))

if __name__ == '__main__':
    main()
