#!/usr/bin/env python3

import sys
import re
import operator

from typing import NamedTuple

OPS = {
    '=': operator.eq,
    '<': operator.lt,
    '>': operator.gt,
}

RULE_PTN = re.compile(r'([xmas])([=<>])(\d+):(\w+)$')
LAST_RULE_PTN = re.compile(r'(\w+)$')
COORD_PTN = re.compile(r'([xmas])=(\d+)$')

class Rule(NamedTuple):
    var: str
    op: callable
    val: int
    target: str

    def __call__(self, part):
        if self.op is None:
            return True
        n = getattr(part, self.var)
        return self.op(n, self.val)

class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

class WorkFlow(NamedTuple):
    name: str
    rules: list

    def __call__(self, part):
        for rule in self.rules:
            if rule(part):
                return rule.target
        raise ValueError("No rule for part %r"%part)

def parse_workflow(name, desc):
    pieces = desc.split(',')
    rules = []
    for piece in pieces[:-1]:
        m = RULE_PTN.match(piece.strip())
        if not m:
            raise ValueError('Workflow rules: %r'%desc)
        var = m.group(1)
        op = OPS[m.group(2)]
        val = int(m.group(3))
        target = m.group(4)
        rules.append(Rule(var, op, val, target))
    m = LAST_RULE_PTN.match(pieces[-1])
    if not m:
        raise ValueError('Workflow rules: %r'%desc)
    target = m.group(1)
    rules.append(Rule(None, None, None, target))
    return WorkFlow(name, rules)

def parse_part(coords):
    kwargs = {}
    for coord in coords:
        m = COORD_PTN.match(coord)
        if not m:
            raise ValueError('Part: %r'%(coords,))
        kwargs[m.group(1)] = int(m.group(2))
    return Part(**kwargs)


def parse_input(lines):
    wf_ptn = re.compile(r'(\w+)\{(.+)\}$')
    part_ptn = re.compile(r'\{X,X,X,X\}'.replace('X', r'\s*([xmas]=\d+)'))
    wfs = {}
    parts = []
    for line in filter(bool, map(str.strip, lines)):
        m = wf_ptn.match(line)
        if m:
            wf = parse_workflow(m.group(1), m.group(2))
            assert wf.name not in wfs
            wfs[wf.name] = wf
        else:
            m = part_ptn.match(line)
            if not m:
                raise ValueError(repr(line))
            parts.append(parse_part(m.groups()))
    return wfs, parts

def process_work(wfs, parts, *, DESTS=set('AR')):
    new_jobs = [(part, 'in') for part in parts]
    output = {'A':[], 'R':[]}
    while new_jobs:
        jobs = new_jobs
        new_jobs = []
        for part, wn in jobs:
            wf = wfs[wn]
            dest = wf(part)
            if dest in DESTS:
                output[dest].append(part)
            else:
                new_jobs.append((part, dest))
    return output

def main():
    lines = sys.stdin.read().strip().splitlines()
    wfs, parts = parse_input(lines)
    output = process_work(wfs, parts)
    rating = sum(sum(part) for part in output['A'])
    print("Part 1:", rating)



if __name__ == '__main__':
    main()
