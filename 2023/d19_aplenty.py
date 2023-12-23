#!/usr/bin/env python3

import sys
import re
import operator

from itertools import product
from collections import defaultdict
from typing import NamedTuple

RULE_PTN = re.compile(r'([xmas])([=<>])(\d+):(\w+)$')
LAST_RULE_PTN = re.compile(r'(\w+)$')
COORD_PTN = re.compile(r'([xmas])=(\d+)$')

LOW = 1
HIGH = 4001

FULL_RANGE = range(LOW, HIGH)

class Rule(NamedTuple):
    var: str
    range: object
    target: str

    def __call__(self, n):
        return (n in self.range)

    def with_target(self, target):
        return Rule(self.var, self.range, target)


class WorkFlow(NamedTuple):
    name: str
    rules: list

    def __call__(self, part):
        for rule in self.rules:
            if rule.var is None or rule(part[rule.var]):
                return rule.target
        raise ValueError("No rule for part %r"%part)

    def can_go(self, ch, n, dest):
        for rule in self.rules:
            if rule.target==dest:
                return rule.var != ch or rule(n)
            if rule.var is None or rule.var==ch and rule(n):
                return False
        return False


class Cuboid:
    def __init__(self, **ranges):
        self.ranges = ranges

    def volume(self):
        n = 1
        for r in self.ranges.values():
            n *= len(r)
        return n


def parse_workflow(name, desc):
    pieces = desc.split(',')
    rules = []
    for piece in pieces[:-1]:
        m = RULE_PTN.match(piece.strip())
        if not m:
            raise ValueError('Workflow rules: %r'%desc)
        var = m.group(1)
        op = m.group(2)
        val = int(m.group(3))
        if op=='=':
            ran = range(val, val+1)
        elif op=='<':
            ran = range(LOW, val)
        elif op=='>':
            ran = range(val+1, HIGH)
        target = m.group(4)
        rules.append(Rule(var, ran, target))
    m = LAST_RULE_PTN.match(pieces[-1])
    if not m:
        raise ValueError('Workflow rules: %r'%desc)
    target = m.group(1)
    rules.append(Rule(None, FULL_RANGE, target))
    return WorkFlow(name, rules)

def parse_part(coords):
    part = {}
    for coord in coords:
        m = COORD_PTN.match(coord)
        if not m:
            raise ValueError('Part: %r'%(coords,))
        part[m.group(1)] = int(m.group(2))
    return part


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

def reverse_targets(wfs):
    wf_sources = defaultdict(list)
    for wf in wfs.values():
        targets = {rule.target for rule in wf.rules}
        for target in targets:
            wf_sources[target].append(wf.name)
    return wf_sources

def find_routes(wf_sources, endpoint):
    routes = []
    sources = wf_sources[endpoint]
    for source in wf_sources[endpoint]:
        if source=='in':
            return [[source,endpoint]]
        for r in find_routes(wf_sources, source):
            routes.append(r + [endpoint])
    return routes

def find_ranges(wfs, route):
    criteria = []
    for i,wf in enumerate(wfs[name] for name in route[:-1]):
        next_target = route[i+1]
        for rule in wf.rules:
            accept = (rule.target==next_target)
            criteria.append((rule, accept))
            if accept and next_target!='A':
                break
    return criteria

def trace_route(wfs, route):
    start = wfs['in']
    current = {ch:FULL_RANGE for ch in 'xmas'}
    for i,wf in enumerate(wfs[name] for name in route[:-1]):
        dest = route[i+1]
        for ch,income in current.items():
            outgo = [n for n in income if wf.can_go(ch, n, dest)]
            current[ch] = outgo

    ranges = {k:convert_to_ranges(v) for k,v in current.items()}
    return list(convert_to_cuboids(ranges))

def convert_to_cuboids(ranges):
    for xr,mr,ar,sr in product(*(ranges[ch] for ch in 'xmas')):
        yield Cuboid(x=xr, m=mr, a=ar, s=sr)

def complete_wfs(wfs):
    acount = 0
    for wf in list(wfs.values()):
        for i, rule in enumerate(wf.rules):
            if rule.target=='A':
                newwf = WorkFlow(f'A{acount}', [Rule(None, FULL_RANGE, 'A')])
                acount += 1
                wfs[newwf.name] = newwf
                wf.rules[i] = rule.with_target(newwf.name)
    return acount

def convert_to_ranges(numbers):
    numbers = sorted(numbers)
    ranges = []
    start = None
    end = None
    for n in numbers:
        if start is None:
            start = end = n
        elif n==end+1:
            end = n
        else:
            ranges.append(range(start, end+1))
            start = end = n
    if end:
        ranges.append(range(start, end+1))
    return ranges

def main():
    lines = sys.stdin.read().strip().splitlines()
    wfs, parts = parse_input(lines)
    complete_wfs(wfs)
    output = process_work(wfs, parts)
    rating = sum(sum(part.values()) for part in output['A'])
    print("Part 1:", rating)
    wf_sources = reverse_targets(wfs)
    a_routes = find_routes(wf_sources, 'A')
    cuboids = []
    for route in a_routes:
        cuboids += trace_route(wfs, route)
    v = sum(c.volume() for c in cuboids)
    print("Part 2:", v)

if __name__ == '__main__':
    main()
