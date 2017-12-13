#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Room = namedtuple('Room', 'letters sector')

def process(line, ptn=re.compile(r'\s*([a-z-]+)-([0-9]+)\[([a-z]+)\]\s*')):
    m = ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    letters = m.group(1)
    sector = int(m.group(2))
    check = m.group(3)
    if check==calc_check(letters):
        return Room(letters, sector)
    return None

def count_letters(seq):
    count = [0]*26
    for ch in seq:
        if 'a'<=ch<='z':
            count[ord(ch)-ord('a')] += 1
    return count

def calc_check(seq, n=5):
    count = count_letters(seq)
    results = []
    for _ in range(0,n):
        m = max(count)
        i = count.index(m)
        results.append(chr(ord('a') + i))
        count[i] = -1
    return ''.join(results)

def decode(room):
    result = []
    for ch in room.letters:
        if 'a'<=ch<='z':
            i = ord(ch)-ord('a')
            i = (i+room.sector)%26
            ch = chr(i+ord('a'))
        result.append(ch)
    return ''.join(result)
    
def find_north_pole(rooms):
    for room in rooms:
        if decode(room)=='northpole-object-storage':
            return room.sector
    return None

def main():
    lines = sys.stdin.read().strip().split('\n')
    rooms = list(filter(bool, map(process, lines)))
    print("Sector sum:", sum(room.sector for room in rooms))
              
    s = find_north_pole(rooms)
    print("North pole:", s)

if __name__ == '__main__':
    main()
