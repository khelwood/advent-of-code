#!/usr/bin/env python3

import sys
import re

def main():
    lines = [line.strip() for line in sys.stdin]
    labels = extract_labels(lines)
    rev_labels = {v:k for (k,v) in labels.items()}
    fixed = [fix_line(line, labels) for line in lines]
    print("#ip 3")
    for i,line in enumerate(fixed):
        label = rev_labels.get(i)
        print(line, '#', end=' ')
        if label:
            print(label+':', end=' ')
        print(lines[i])
        
def match(ptn, line):
    return re.match(ptn.replace(' ', r'\s*')
                        .replace('%', '([A-Z])')
                        .replace('#', r'(-?\d+)') + '$', line)
        
def extract_labels(lines):
    i = 0
    labels = {}
    while i < len(lines):
        line = lines[i]
        m = re.match(r'(\w+):', line)
        if m:
            labels[m.group(1)] = i
            del lines[i]
        else:
            i += 1
    return labels

def fix_line(line, labels):
    vtn = dict(zip('ABCEF', (0,1,2,4,5)))
    m = match(r'GOTO (\w+)', line)
    if m:
        index = labels[m.group(1)]-1
        return f'seti {index} 0 3'
    m = match('% = %', line)
    if m:
        c = vtn[m.group(1)]
        a = vtn[m.group(2)]
        return f'setr {a} 0 {c}'
    m = match('% = #', line)
    if m:
        c = vtn[m.group(1)]
        a = m.group(2)
        return f'seti {a} 0 {c}'
    m = match(r'% \+= %', line)
    if m:
        c = vtn[m.group(1)]
        a = vtn[m.group(2)]
        return f'addr {c} {a} {c}'
    m = match(r'% \+= #', line)
    if m:
        c = vtn[m.group(1)]
        a = m.group(2)
        return f'addi {c} {a} {c}'
    m = match(r'% = \( % > % \)', line)
    if m:
        c,a,b = (vtn[g] for g in m.groups())
        return f'gtrr {a} {b} {c}'
    m = match('% = \( % ==? % \)', line)
    if m:
        c,a,b = (vtn[g] for g in m.groups())
        return f'eqrr {a} {b} {c}'
    m = match('IF % SKIP', line)
    if m:
        b = vtn[m.group(1)]
        return f'addr 3 {b} 3'
    if line=='SKIP':
        return 'addi 3 1 3'
    if line=='END':
        return 'seti 999 0 3'
    raise ValueError(repr(line))
    

if __name__ == '__main__':
    main()
