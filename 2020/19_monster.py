#!/usr/bin/env python3

import sys
import re

T_OR = '|'
T_CH = 'C'
T_SEQ = '+'
T_INT = '#'

from collections import namedtuple

Node = namedtuple('Node', 'type value')

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

def match(typ, value, code, rulebook):
    if typ==T_CH:
        if code and code[0]==value:
            yield 1
        return
    if typ==T_SEQ:
        if len(value)==0:
            yield 0
            return
        first = value[0]
        firstmatch = match(first.type, first.value, code, rulebook)
        if len(value)==1:
            yield from firstmatch
        else:
            rest = value[1:]
            for c in firstmatch:
                for r in match(typ, rest, code[c:], rulebook):
                    yield c+r
        return
    if typ==T_OR:
        for val in value:
            yield from match(val.type, val.value, code, rulebook)
        return
    if typ==T_INT:
        rule = rulebook[value]
        yield from match(rule.type, rule.value, code, rulebook)
        return

def match_rule(rule, rulebook, code):
    lc = len(code)
    for n in match(rule.type, rule.value, code, rulebook):
        if n==lc:
            return True
    return False

def lex(rule):
    i = 0
    lr = len(rule)
    while i < lr:
        ch = rule[i]
        if ch=='|':
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

def assemble(tokens):
    i = find(tokens, '|')
    if i >= 0:
        return Node(T_OR, [assemble(tokens[:i]), assemble(tokens[i+1:])])
    if len(tokens)==1:
        token, = tokens
        typ = T_INT if isinstance(token, int) else T_CH
        return Node(typ, token)
    return Node(T_SEQ, [assemble([tok]) for tok in tokens])

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
        tokens = list(lex(rule))
        node = assemble(tokens)
        rulebook[index] = node
    codes = list(map(str.strip, sys.stdin))
    assert all(i in rulebook for i in range(len(rulebook)))
    rulebook = [rulebook[k] for k in sorted(rulebook)]
    return rulebook, codes

def main():
    rulebook, codes = parse_input()
    rule = rulebook[0]
    total = sum(match_rule(rule, rulebook, code) for code in codes)
    print("Matches (no loops):", total)
    rulebook[8] = assemble(list(lex('42 | 42 8')))
    rulebook[11] = assemble(list(lex('42 31 | 42 11 31')))
    total = sum(match_rule(rule, rulebook, code) for code in codes)
    print("Matches (with loops):", total)

if __name__ == '__main__':
    main()
