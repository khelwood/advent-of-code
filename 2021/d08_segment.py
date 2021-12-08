#!/usr/bin/env python3

import sys

def read_words(line):
    a,_,b = line.partition('|')
    return tuple(tuple(frozenset(w) for w in x.split()) for x in (a,b))

def deduce_signals(words):
    words = set(words)
    codes = [None]*10
    for (n, ln) in ((1,2), (7,3), (4,4), (8,7)):
        codes[n] = next(w for w in words if len(w)==ln)
        words.remove(codes[n])
    top_bit, = codes[7] - codes[1]
    x,y = codes[1]
    if sum(x in w for w in words)==4:
        x,y = y,x
    br_bit, tr_bit = x,y
    codes[6] = next(w for w in words if len(w)==6 and tr_bit not in w)
    words.remove(codes[6])
    codes[3] = next(w for w in words if len(w)==5 and tr_bit in w and br_bit in w)
    words.remove(codes[3])
    # remaining: 0, 2, 5, 9
    codes[5] = next(w for w in words if len(w)==5 and tr_bit not in w)
    words.remove(codes[5])
    # remaining: 0, 2, 9
    bl_bit = next(c for c in codes[6] if c not in codes[5])
    codes[9] = next(w for w in words if len(w)==6 and bl_bit not in w)
    words.remove(codes[9])
    # remaining: 0, 2
    codes[0] = next(w for w in words if len(w)==6)
    words.remove(codes[0])
    codes[2], = words
    return {w:num for (num,w) in enumerate(codes)}

def main():
    data = tuple(map(read_words, sys.stdin.read().strip().splitlines()))
    simple_pattern_sizes = {2,3,4,7}
    simple_count = sum(len(word) in simple_pattern_sizes
                       for (_, words) in data for word in words)
    print("Simple count:", simple_count)
    total = 0
    for words, output in data:
        decodes = deduce_signals(words)
        result = int(''.join(map(str, (decodes[w] for w in output))))
        total += result
    print("Total output:", total)

if __name__ == '__main__':
    main()
