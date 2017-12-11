#!/usr/bin/env python3

import re

ord_a=ord('a')

def process(line, ptn=re.compile(r'\s*([a-z-]+)-([0-9]+)\[([a-z]+)\]\s*')):
    m = ptn.match(line)
    if not m:
        raise ValueError(line)
    letters = m.group(1)
    sector = int(m.group(2))
    check = m.group(3)
    if check==calc_check(letters):
        return letters, sector
    return None

def count_letters(seq):
    count = [0]*26
    for ch in seq:
        if 'a'<=ch<='z':
            count[ord(ch)-ord_a] += 1
    return count

def calc_check(seq, n=5):
    count = count_letters(seq)
    results = []
    for _ in range(0,n):
        m = max(count)
        i = count.index(m)
        results.append(chr(ord_a + i))
        count[i] = -1
    return ''.join(results)

def main():
    import pyperclip
    block = pyperclip.paste()
    lines = [x for x in (x.strip() for x in block.split('\n')) if x]
    s = find_north_pole(lines)
    print(f"North pole is at {s}")

def decode(letters, sector):
    sector %= 26
    result = []
    for ch in letters:
        if 'a'<=ch<='z':
            i = ord(ch)-ord_a
            i = (i+sector)%26
            ch = chr(i+ord_a)
        result.append(ch)
    return ''.join(result)
            
    
def find_north_pole(lines):
    for letters, sector in filter(bool, map(process, lines)):
        decoded = decode(letters, sector)
        if decoded=='northpole-object-storage':
            return sector
    return None

if __name__ == '__main__':
    main()
