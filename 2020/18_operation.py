#!/usr/bin/env python3

import sys

def lex(line):
    line = line.strip()
    i = 0
    end = len(line)
    while i < end:
        ch = line[i]
        if ch.isspace():
            i += 1
            continue
        if ch in '*+()':
            yield ch
            i += 1
            continue
        j = i+1
        while j < end and line[j].isdigit():
            j += 1
        yield int(line[i:j])
        i=j

def lex_input():
    return [tuple(lex(line)) for line in sys.stdin]

def find_end(tokens, start):
    depth = 1
    i = start
    while True:
        i += 1
        tok = tokens[i]
        if tok==')':
            depth -= 1
            if depth==0:
                return i
        elif tok=='(':
            depth += 1
    raise ValueError("Unbalanced parentheses in %r"%tokens)

def evaluate_ltr(tokens, start=0, end=None):
    if end is None:
        end = len(tokens)
    i = start
    current = tokens[i]
    if current=='(':
        j = find_end(tokens, i)
        current = evaluate_ltr(tokens, i+1, j)
        i = j
    i += 1
    while i < end:
        op = tokens[i]
        i += 1
        new = tokens[i]
        if new=='(':
            j = find_end(tokens, i)
            new = evaluate_ltr(tokens, i+1, j)
            i = j
        if op=='+':
            current += new
        elif op=='*':
            current *= new
        else:
            raise ValueError("Expected operation but got %r"%op)
        i += 1
    return current

def evaluate_pm(tokens):
    while '(' in tokens:
        j = tokens.index(')')
        i = j-1
        while tokens[i]!='(':
            i -= 1
        tokens[i:j+1] = [evaluate_pm(tokens[i+1:j])]
    while '+' in tokens:
        i = tokens.index('+')
        tokens[i-1:i+2] = [tokens[i-1] + tokens[i+1]]
    while '*' in tokens:
        i = tokens.index('*')
        tokens[i-1:i+2] = [tokens[i-1] * tokens[i+1]]
    assert len(tokens)==1
    return tokens[0]

def main():
    expressions = lex_input()
    ltr = sum(map(evaluate_ltr, expressions))
    print("Total (left to right):", ltr)
    pm = sum(evaluate_pm(list(ex)) for ex in expressions)
    print("Total (plus first):", pm)

if __name__ == '__main__':
    main()
