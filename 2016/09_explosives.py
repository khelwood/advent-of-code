#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

MARKER_PTN = re.compile(r'\(([0-9]+)x([0-9]+)\)')

class Sub:
    def __init__(self, match):
        self.start = match.start()
        self.end = match.end()
        self.reach = int(match.group(1))
        self.repeats = int(match.group(2))
        self.mass = None

def simple_decompress_length(data):
    total = 0
    j = 0
    m = MARKER_PTN.search(data)
    while m:
        total += m.start()-j
        num = int(m.group(1))
        reps = int(m.group(2))
        j = m.end()+num
        total += num*reps
        m = MARKER_PTN.search(data, j)
    total += len(data)-j
    return total

def extract_pieces(data):
    pieces = []
    j = 0
    for m in MARKER_PTN.finditer(data):
        if m.start() > j:
            pieces.append(m.start()-j)
        pieces.append(Sub(m))
        j = m.end()
    if j < len(data):
        pieces.append(len(data)-j)
    return pieces

def mass(x):
    return x.mass if isinstance(x, Sub) else x

def span(x):
    return (x.end-x.start) if isinstance(x, Sub) else x

def combine_markers(pieces, pos, reach):
    """Find all the markers and text within the reach of a marker,
    in order to calculate its combined mass."""
    total_mass = 0
    while reach > 0:
        pos += 1
        piece = pieces[pos]
        piece_span = span(piece)
        if piece_span==reach:
            return total_mass + mass(piece)
        if piece_span > reach:
            return total_mass + n
        reach -= piece_span
        total_mass += mass(piece)
    return total_mass

def reverse_enumerate(items):
    return zip(range(len(items)-1, -1, -1), reversed(items))

def complex_decompress_length(data):
    pieces = extract_pieces(data)
    for i, cur in reverse_enumerate(pieces):
        if mass(cur) is None:
            m = combine_markers(pieces, i, cur.reach)
            cur.mass = (cur.repeats-1) * m
    return sum(map(mass, pieces))

def main():
    data = re.sub(r'\s+', '', sys.stdin.read())
    length = simple_decompress_length(data)
    print("Simple decompress length:", length)
    length = complex_decompress_length(data)
    print("Complex decompress length:", length)

if __name__ == '__main__':
    main()
