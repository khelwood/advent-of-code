#!/usr/bin/env python3

import sys
import re

from functools import reduce
from itertools import chain
from dataclasses import dataclass

NUM_PTN = re.compile(r'\d+')
NAME_PTN = re.compile(r'(\w+)-to-(\w+) map:')

@dataclass(frozen=True)
class Span:
    key_span: tuple
    diff: int

    @property
    def key_start(self):
        return self.key_span[0]

    @property
    def key_end(self):
        return self.key_span[1]

    @property
    def value_span(self):
        a,b = self.key_span
        d = self.diff
        return (none_add(a, d), none_add(b, d))

    @property
    def value_start(self):
        return none_add(self.key_start, self.diff)

    @property
    def value_end(self):
        return none_add(self.key_end, self.diff)

    def __contains__(self, k):
        return in_bounds(self.key_span, k)

    def contains_value(self, v):
        return (v-self.diff) in self

    def __lt__(self, other):
        if not isinstance(other, Span):
            return NotImplemented
        s, s1 = self.key_span
        t, t1 = other.key_span
        if s != t:
            if s is None:
                return True
            if t is None:
                return False
            return (s < t)
        if s1==t1:
            return False
        if s1 is None:
            return False
        if t1 is None:
            return True
        return s1 < t1

    def get(self, k, default=None):
        return (k + self.diff) if k in self else default

    def get_back(self, v, default=None):
        v -= self.diff
        return v if v in self else default

    def __len__(self):
        a,b = self.key_span
        if a is None or b is None:
            return None
        return b-a

    def cmp_key(self, k):
        a,b = self.key_span
        if a is not None and k < a:
            return 1 # span is above key
        if b is not None and k >= b:
            return -1 # span is below key
        return 0 # span contains key

    def __and__(self, other):
        if not isinstance(other, Span):
            return NotImplemented
        start, end = self.key_span
        ostart, oend = other.key_span
        diff = self.diff
        if start is None:
            start = None if ostart is None else (ostart - diff)
        elif ostart is not None:
            start = max(start, ostart - diff)
        if end is None:
            end = None if oend is None else (oend - diff)
        elif oend is not None:
            end = min(end, oend - diff)
        return Span((start, end), diff + other.diff)

def none_add(a,b):
    return (None if a is None else (a+b))

def in_bounds(bounds, value):
    a,b = bounds
    if a is not None and a > value:
        return False
    if b is not None and b <= value:
        return False
    return True

@dataclass(frozen=True)
class DiffMap:
    keyname: str
    valuename: str
    spans: tuple

    def __getitem__(self, k):
        i = self.span_index(k)
        return self.spans[i].get(k)

    def span_index(self, k):
        left = 0
        spans = self.spans
        right = len(spans)
        while left < right:
            middle = (left + right)//2
            span = spans[middle]
            n = span.cmp_key(k)
            if n < 0:
                left = middle+1
                continue
            elif n > 0:
                right = middle
                continue
            return middle
        raise ValueError(f'no span for {k} in {self}')

    def value_span(self, v):
        return next(s for s in self.spans if s.contains_value(v))

    def get_back(self, v) -> list:
        keys = []
        for span in spans:
            k = span.get_back(v)
            if k is not None:
                keys.append(k)
        return keys

    def __str__(self):
        return f'{self.keyname}-to-{self.valuename}'

def make_map(kn, vn, spans):
    spans = [Span((b, b+c), a-b) for (a,b,c) in spans]
    spans.sort()
    more_spans = []
    top = None
    for span in spans:
        s0, s1 = span.key_span
        if top is None or s0 > top:
            more_spans.append(Span((top, s0), 0))
        more_spans.append(span)
        top = s1
    if top:
        more_spans.append(Span((top, None), 0))
    return DiffMap(kn, vn, tuple(more_spans))

def parse_diffmaps(lines):
    line_iter = filter(bool, map(str.strip, lines))
    line = next(line_iter)
    assert line.startswith('seeds: ')
    line = line[7:]
    seeds = tuple(map(int, NUM_PTN.findall(line)))
    maps = []
    kn = None
    for line in line_iter:
        m = NAME_PTN.match(line)
        if m:
            if kn:
                maps.append(make_map(kn, vn, spans))
            kn,vn = m.groups()
            spans = []
        else:
            nums = tuple(map(int, NUM_PTN.findall(line)))
            if len(nums)!=3:
                raise ValueError(repr(nums))
            assert len(nums)==3
            spans.append(nums)
    if kn:
        maps.append(make_map(kn, vn, spans))
    return seeds, maps

def merge_maps(ma, mb):
    assert ma.valuename==mb.keyname
    spans = []
    for a in ma.spans:
        v0,v1 = a.value_span
        bi = mb.span_index(v0) if v0 is not None else 0
        bj = mb.span_index(v1) if v1 is not None else len(mb.spans)-1
        if bi==bj:
            b = mb.spans[bi]
            spans.append(Span(a.key_span, a.diff + b.diff))
            continue
        for i in range(bi, bj+1):
            spans.append(a & mb.spans[i])
    return DiffMap(ma.keyname, mb.valuename, tuple(spans))

def seed_iter(seeds):
    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append(range(seeds[i], seeds[i]+seeds[i+1]))
    return chain.from_iterable(ranges)

def make_seed_map(seeds):
    k = seeds[1]
    spans = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        length = seeds[i+1]
        spans.append(Span((k, k+length), start-k))
        k += length
    return DiffMap('index', 'seed', tuple(spans))


def main():
    seeds, maps = parse_diffmaps(sys.stdin.read().strip().splitlines())
    combined_map = reduce(merge_maps, maps)
    m = min(combined_map[seed] for seed in seeds)
    print("Part 1:", m)
    seed_map = make_seed_map(seeds)
    combined_map = merge_maps(seed_map, combined_map)
    m = min(combined_map[span.key_start] for span in combined_map.spans)
    print("Part 2:", m)


if __name__ == '__main__':
    main()
