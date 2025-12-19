#!/usr/bin/env python3

import sys

from itertools import combinations

def crosses(line1, line2):
    ((minx1, miny1), (maxx1, maxy1)) = line1
    ((minx2, miny2), (maxx2, maxy2)) = line2
    if miny1==maxy1:
        return (minx2==maxx2 and minx1 <= minx2 <= maxx1
                and miny2 <= miny1 <= maxy2)
    else:
        return (miny2==maxy2 and miny1 <= miny1 <= maxy1
                and minx2 <= minx1 <= maxx2)
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
        x0,y0=cur
        x1,y1=last
        if x1 < x0:
            x1,x0 = x0,x1
        if y1 < y0:
            y1,y0 = y0,y1
        edges.append(((x0,y0),(x1,y1)))
        last = cur
    return edges

def rect_corners(a,c):
    ax,ay = a
    cx,cy = c
    b = (ax,cy)
    d = (cx,ay)
    return (a,b,c,d)

def find_best_area(reds):
    edges = find_edges(reds)
    best = 0

    for a,b in combinations(reds, 2):
        ax,ay = a
        bx,by = b
        if ax==bx or ay==by:
            continue
        area = rect_area(a,b)
        if area <= best:
            continue
        good = True
        sides = find_edges(rect_corners(a,b))
        if bx < ax:
            ax,bx = bx,ax
        if by < ay:
            ay,by = by,ay
        for edge in edges:
            (eminx,eminy), (emaxx,emaxy) = edge
            if (emaxx <= ax or eminx >= bx or emaxy <= ay or eminy >= by):
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
