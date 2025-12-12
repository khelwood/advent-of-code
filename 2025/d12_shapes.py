#!/usr/bin/env python3

import sys

from dataclasses import dataclass

@dataclass
class Shape:
    wid: int
    hei: int
    cells: frozenset

@dataclass
class Region:
    wid: int
    hei: int
    presents: tuple

class ShapeGroup(list):
    @property
    def volume(self):
        return len(self[0].cells)

def parse_region(line):
    i = line.index(':')
    wid, _, hei = line[:i].partition('x')
    wid, hei = map(int, (wid, hei))
    presents = tuple(map(int, line[i+1:].strip().split()))
    return Region(wid=wid, hei=hei, presents=presents)

def parse_shape(line_iter):
    cells = set()
    for y,line in enumerate(line_iter):
        if not line:
            hei = y
            break
        wid = len(line)
        for x,ch in enumerate(line):
            if ch=='#':
                cells.add((x,y))
    return Shape(wid=wid, hei=hei, cells=frozenset(cells))

def read_input():
    line_iter = map(str.strip, sys.stdin)
    shapes = []
    regions = []
    for line in filter(bool, line_iter):
        assert ':' in line
        if 'x' in line:
            regions.append(parse_region(line))
        else:
            shapes.append(parse_shape(line_iter))
    return shapes, regions

def flip(shape):
    x1 = shape.wid - 1
    return Shape(shape.wid, shape.hei, frozenset((x1-x, y) for (x,y) in shape.cells))

def rotate(shape):
    y1 = shape.hei - 1
    return Shape(shape.hei, shape.wid, frozenset((y1-y, x) for (x,y) in shape.cells))

def make_shape_group(index, shape):
    group = ShapeGroup()
    group.index = index
    group.append(shape)
    flipped = flip(shape)
    if flipped.cells==shape.cells:
        flipped = None
    else:
        group.append(flipped)
    for _ in range(3):
        shape = rotate(shape)
        if not any(shape.cells==sh.cells for sh in group):
            group.append(shape)
        if flipped:
            flipped = rotate(flipped)
            if not any(flipped.cells==sh.cells for sh in group):
                group.append(flipped)
    return group

def select_presents(presents, groups):
    results = []
    for i,n in enumerate(presents):
        if n > 0:
            results += [groups[i]] * n
    return results

def fit_shapes(region, groups):
    groups = select_presents(region.presents, groups)
    filled = frozenset()
    return fit_rec(region.wid, region.hei, filled, groups)

def fit_rec(wid, hei, filled, groups, *, _cache={}):
    if not groups:
        return True
    key = (wid, hei, tuple(g.index for g in groups), filled)
    if key in _cache:
        return _cache[key]
    group = groups[0]
    rest = groups[1:]
    for sh in group:
        for x in range(wid+1-sh.wid):
            for y in range(hei+1-sh.hei):
                new = try_fit(sh, x, y, filled)
                if new and fit_rec(wid, hei, new, rest):
                    _cache[key] = True
                    return True
    _cache[key] = False
    return False

def try_fit(shape, x0, y0, filled, *, _cache={}):
    key = (shape.cells, x0, y0, filled)
    if key in _cache:
        return _cache[key]
    new = set(filled)
    for x,y in shape.cells:
        p = (x0+x, y0+y)
        if p in new:
            _cache[key] = None
            return None
        new.add(p)
    new = frozenset(new)
    _cache[key] = new
    return new

def plausible(r, groups):
    required_area = 0
    for group, n in zip(groups, r.presents):
        required_area += n * group.volume
    return (required_area <= r.wid*r.hei)

def easy(r):
    return ((r.wid//3) * (r.hei//3) >= sum(r.presents))

def main():
    shapes, regions = read_input()
    groups = [make_shape_group(i, shape) for (i,shape) in enumerate(shapes)]
    easy_regions = []
    plausible_regions = []
    for r in regions:
        if easy(r):
            easy_regions.append(r)
        elif plausible(r, groups):
            plausible_regions.append(r)
    print("Num easy regions:", len(easy_regions))
    print("Num complex plausible regions:", len(plausible_regions))
    print("Num implausible regions:", len(regions)-len(easy_regions)-len(plausible_regions))
    answer = len(easy_regions)
    if plausible_regions:
        print("Checking plausible regions ...")
        answer += sum(fit_shapes(r, groups) for r in plausible_regions)
    print("Answer:", answer)


if __name__ == '__main__':
    main()
