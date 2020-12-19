#!/usr/bin/env python3

import sys
import re

def parse_input():
    ptn = re.compile(r'^(\d+):\s*(.+)$')
    rulebook = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        m = re.match(ptn, line)
        index = int(m.group(1))
        rule = m.group(2)
        rulebook[index] = tuple(lex(rule))
    codes = list(map(str.strip, sys.stdin))
    assert all(i in rulebook for i in range(len(rulebook)))
    rulebook = [rulebook[k] for k in sorted(rulebook)]
    return rulebook, codes

def rindex(seq, value, start=0, end=None):
    if end is None:
        end = len(seq)
    for i in range(end-1, start, -1):
        if seq[i]==value:
            return i
    raise ValueError("Element not found")

def find(seq, value, start=0, end=None):
    if end is None:
        end = len(seq)
    for i in range(start, end):
        if seq[i]==value:
            return i
    return -1

def can_concrete(rule, rulebook):
    return all(isinstance(rulebook[tok], str)
                for tok in rule if isinstance(tok, int))

def concrete_rules(rulebook):
    improved = False
    for i,rule in enumerate(rulebook):
        if not isinstance(rule, str) and can_concrete(rule, rulebook):
            rulebook[i] = concrete(rule, rulebook)
            improved = True
    return improved

def concrete(rule, rulebook):
    if len(rule)==1:
        tok, = rule
        if isinstance(tok, str):
            return tok
        return rulebook[tok]
    i = find(rule, '|')
    if i >= 0:
        return (f'({concrete(rule[:i], rulebook)}|'
                f'{concrete(rule[i+1:], rulebook)})')
    return '('+''.join([rulebook[tok] for tok in rule])+')'

def lex(rule):
    i = 0
    lr = len(rule)
    while i < lr:
        ch = rule[i]
        if ch in '()|':
            yield ch
            i += 1
        elif ch.isdigit():
            j = i + 1
            while j < lr and rule[j].isdigit():
                j += 1
            yield int(rule[i:j])
            i = j
        elif ch=='"':
            assert rule[i+1]!=ch
            assert rule[i+2]==ch
            yield rule[i+1]
            i += 3
        elif ch.isspace():
            i += 1
        else:
            raise ValueError(repr(rule))
    

def main():
    rulebook, codes = parse_input()
    while concrete_rules(rulebook):
        pass
    main_rule = re.compile('^(' + rulebook[0] + ')$')
    match_count = sum(re.match(main_rule, code) is not None for code in codes)
    print("Match count:", match_count)

if __name__ == '__main__':
    main()
