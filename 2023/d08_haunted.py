#!/usr/bin/env python3

import sys
import re

from itertools import cycle
from typing import NamedTuple

NODE_PTN = re.compile(r'$ = \($, $\)'
    .replace(' ', r'\s*').replace('$', r'(\w+)'))

def parse_input(lines, LR={'L':0, 'R':1}):
    line_iter = filter(bool, map(str.strip, lines))
    line = next(line_iter)
    route = tuple(LR[c] for c in line)
    nodes = {}
    for line in line_iter:
        m = NODE_PTN.match(line)
        if not m:
            raise ValueError(repr(line))
        key = m.group(1)
        left = m.group(2)
        right = m.group(3)
        nodes[key] = (left, right)
    return route, nodes

def follow_route(nodes, basicroute, start):
    steps = 0
    cur = start
    route = cycle(basicroute)
    while True:
        yield steps, cur
        steps += 1
        cur = nodes[cur][next(route)]

class HitCycle(NamedTuple):
    intro: int
    intro_hits: set
    period: int
    period_hits: set

    def iter_hits(self):
        yield from self.intro_hits
        n = self.intro
        p = self.period
        while True:
            for h in self.period_hits:
                yield h + n
            n += p

    def has_hit(self, n):
        if n in self.intro_hits:
            return True
        if n <= self.intro:
            return False
        n -= self.intro
        n %= self.period
        return (n in self.period_hits)


def main():
    basicroute, nodes = parse_input(sys.stdin.read().splitlines())
    routelength = len(basicroute)
    cur = 'AAA'
    if cur in nodes:
        for steps, cur in follow_route(nodes, basicroute, cur):
            if cur=='ZZZ':
                break
        print("Part 1:", steps)
    starts = [node for node in nodes if node.endswith('A')]
    hitcycles = []
    for start in starts:
        router = follow_route(nodes, basicroute, start)
        seen = set()
        intro_hits = set()
        hits = set()
        for steps, cur in router:
            if cur.endswith('Z'):
                intro_hits.add(steps)
            key = (cur, steps%routelength)
            if key in seen:
                intro = steps
                start = key
                if cur.endswith('Z'):
                    hits.add(0)
                break
            seen.add(key)
        for steps, cur in router:
            key = (cur, steps%routelength)
            if cur.endswith('Z'):
                hits.add(steps-intro)
            if key==start:
                break
        period = steps - intro
        hitcycles.append(HitCycle(intro, intro_hits, period, hits))


    hitcycles.sort(key=lambda hc: -hc.period)
    longest = hitcycles[0]
    next_longest = hitcycles[1]
    for n in longest.iter_hits():
        if next_longest.has_hit(n):
            step = n
            break
    for hc in hitcycles[2:]:
        while not hc.has_hit(n):
            n += step
        step = n
    assert all(hc.has_hit(n) for hc in hitcycles)
    print('Part 2:', n)


if __name__ == '__main__':
    main()
