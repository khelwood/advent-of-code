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
HIGH = 4000

FULL_RANGE = range(LOW, HIGH+1)

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
            ran = range(val+1, HIGH+1)
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


def follow_all(wfs):
    end_ptn = re.compile(r'A\d+')
    output = defaultdict(dict)
    for ch in 'xmas':
        income = {}
        queue = ['in']
        income['in'] = FULL_RANGE
        while queue:
            name = queue.pop(0)
            if name=='R':
                continue
            if end_ptn.fullmatch(name):
                output[name][ch] = income[name]
                continue
            wf = wfs[name]
            remaining = set(income[name])
            for rule in wf.rules:
                if rule.var==ch:
                    values = remaining
                    out = set()
                    remaining = set()
                    for n in values:
                        (out if rule(n) else remaining).add(n)
                else:
                    out = remaining
                if out:
                    income[rule.target] = out
                    queue.append(rule.target)
    return output

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

def compute_volume(output):
    volume = 0
    for dest, coords in output.items():
        if len(coords)==4:
            n = 1
            for ch in 'xmas':
                n *= len(coords[ch])
            volume += n
    return volume

def main():
    lines = sys.stdin.read().strip().splitlines()
    wfs, parts = parse_input(lines)
    complete_wfs(wfs)
    output = process_work(wfs, parts)
    rating = sum(sum(part.values()) for part in output['A'])
    print("Part 1:", rating)
    output = follow_all(wfs)
    vol = compute_volume(output)
    print("Part 2:", vol)

if __name__ == '__main__':
    main()
