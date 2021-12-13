#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Fold = namedtuple('Fold', 'axis pos')

def read_data():
    lines = sys.stdin.read().strip().splitlines()
    dots = set()
    folds = []
    fptn = re.compile(r'fold along ([xy])=(\d+)$')
    for line in lines:
        if line.startswith('fold'):
            m = fptn.match(line)
            folds.append(Fold(axis='xy'.index(m.group(1)), pos=int(m.group(2))))
        elif ',' in line:
            x,_,y = line.partition(',')
            dots.add((int(x), int(y)))
    return dots, folds

def apply_fold(fold, dots):
    new = set()
    axis = fold.axis
    pos = fold.pos
    for dot in dots:
        if dot[axis] > pos:
            refl = 2*pos - dot[axis]
            if axis==0:
                dot = (refl, dot[1])
            else:
                dot = (dot[0], refl)
        new.add(dot)
    return new

def draw_dots(dots, wid, hei):
    xs = range(wid)
    for y in range(hei):
        for x in xs:
            print('#' if (x,y) in dots else ' ', end='')
        print()

def main():
    dots, folds = read_data()
    dots = apply_fold(folds[0], dots)
    print("Num dots:", len(dots))
    maxes = [0,0]
    for fold in folds[1:]:
        dots = apply_fold(fold, dots)
        maxes[fold.axis] = fold.pos
    draw_dots(dots, *maxes)

if __name__ == '__main__':
    main()
