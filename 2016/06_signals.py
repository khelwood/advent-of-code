#!/usr/bin/env python3

import sys

def extract_letter(letters, use_min=False):
    counts = [0]*26
    for ch in letters:
        counts[ord(ch)-ord('a')] += 1
    if use_min:
        m = min(filter(bool, counts))
    else:
        m = max(counts)
    i = counts.index(m)
    return chr(ord('a')+i)

def main():
    lines = sys.stdin.read().strip().split('\n')
    columns = list(zip(*lines))
    message = ''.join(map(extract_letter, columns))
    print("First message:", message)
    message = ''.join([extract_letter(letters, True) for letters in columns])
    print("Second message:", message)

if __name__ == '__main__':
    main()
