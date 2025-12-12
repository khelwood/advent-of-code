#!/usr/bin/env python3

import sys

from itertools import combinations

def between(v, a, b):
    return (a <= v <= b) if (a <= b) else (b <= v <= a)

def horizontal(line):
    return line[0][1]==line[1][1]

def vertical(line):
    return line[0][0]==line[1][0]

def crosses(line1, line2):
    if horizontal(line1):
        return (vertical(line2) and between(line2[0][0], line1[0][0], line1[1][0])
                and between(line1[0][1], line2[0][1], line2[1][1]))
    else:
        return (horizontal(line2) and between(line2[0][1], line1[0][1], line1[1][1])
                and between(line1[0][0], line2[0][0], line2[1][0]))
    return False

def read_input():
    lines = filter(bool, map(str.strip, sys.stdin))
    return [tuple(map(int, s.split(','))) for s in lines]

def rect_area(a,b):
    ax,ay = a
    bx,by = b
    return (abs(ax-bx)+1)*(abs(ay-by)+1)

def find_edges(points):
    last = points[-1]
    edges = []
    for cur in points:
        edges.append((last, cur))
        last = cur
    return edges

def rect_corners(a,c):
    b = (a[0],c[1])
    d = (c[0],a[1])
    return (a,b,c,d)

def find_best_area(reds):
    edges = find_edges(reds)
    edge_min = [tuple(min(pt[i] for pt in ln) for i in (0,1)) for ln in edges]
    edge_max = [tuple(max(pt[i] for pt in ln) for i in (0,1)) for ln in edges]
    best = 0

    for a,b in combinations(reds, 2):
        if a[0]==b[0] or a[1]==b[1]:
            continue
        area = rect_area(a,b)
        if area <= best:
            continue
        good = True
        sides = find_edges(rect_corners(a,b))
        xmin = min(a[0],b[0])
        xmax = max(a[0],b[0])
        ymin = min(a[1],b[1])
        ymax = max(a[1],b[1])
        for (emnx, emny), (emxx, emxy), edge in zip(edge_min, edge_max, edges):
            if (emxx <= xmin or emnx >= xmax or emxy <= ymin or emny >= ymax):
                continue
            if any(crosses(side, edge) for side in sides):
                good = False
                break
        if good:
            best = area
    return best

def main():
    reds = read_input()
    print(max(rect_area(a,b) for (a,b) in combinations(reds, 2)))
    print(find_best_area(reds))

if __name__ == '__main__':
    main()
