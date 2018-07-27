#!/usr/bin/env python3

import sys
import re

from collections import Counter

class Entry:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = tuple(children)
        self.parent = None
    @property
    def balanced(self):
        try:
            return self._balanced
        except AttributeError:
            self._balanced = (len(self.children) <= 1 or
                 all_eq(c.total_weight for c in self.children))
        return self._balanced
    @property
    def total_weight(self):
        try:
            return self._total_weight
        except AttributeError:
            self._total_weight = self.weight + sum(c.total_weight for c in self.children)
        return self._total_weight

def all_eq(seq, sentinel=object()):
    it = iter(seq)
    v = next(it, sentinel)
    return v is sentinel or all(x==v for x in it)

def make_entry(line, pattern=re.compile(r'(\w+)\s*\((\d+)\)\s*$')):
    line, _, cline = line.partition('->')
    m = pattern.match(line)
    name = m.group(1)
    weight = int(m.group(2))
    children = tuple(cline.replace(',',' ').split())
    return Entry(name, weight, children)

def read_entries():
    edict = { e.name: e for e in map(make_entry, sys.stdin) }
    # link children and parents
    for e in edict.values():
        e.children = tuple(edict[c] for c in e.children)
        for c in e.children:
            c.parent = e
    return tuple(edict.values())

def find_weight_error(entries):
    """Find the amount (positive or negative) by which the
    incorrect weight is incorrect."""
    e = next(e for e in entries
                 if len(e.children)>=3 and not e.balanced)
    c = Counter(ec.total_weight for ec in e.children)
    correct_weight = next(k for k,v in c.items() if v>1)
    incorrect_weight = next(k for k,v in c.items() if v==1)
    return incorrect_weight - correct_weight

def correct_weight(entries):
    """Find the correct weight of whichever weight is incorrect."""
    error = find_weight_error(entries)

    # Find the parent which is imbalanced but all its children are balanced
    error_parent = next(e for e in entries
                    if not e.balanced and all(c.balanced for c in e.children))
    # Find the anomalous entry
    bad_entry = (max if error > 0 else min)(error_parent.children,
                                  key=lambda ec : ec.total_weight)
    return bad_entry.weight - error

def main():
    entries = read_entries()
    root = next(e for e in entries if not e.parent)
    print("Root:", root.name)
    print("Correct weight:", correct_weight(entries))

if __name__ == '__main__':
    main()
