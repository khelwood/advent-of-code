#!/usr/bin/env python3

import sys
import re
import itertools
from collections import defaultdict

def manhattan(a,b):
    return (abs(a[0]-b[0]) + abs(a[1]-b[1]))

def read_input(srcfile):
    sensor_beacons = {}
    ptn = re.compile(r'[xy]=(-?\d+)')
    with open(srcfile) as fin:
        for line in fin.read().strip().splitlines():
            x0,y0, x1,y1 = map(int, re.findall(ptn, line))
            sensor_beacons[x0,y0] = x1,y1
    return sensor_beacons

def find_bounds(points):
    it = iter(points)
    x0,y0 = x1,y1 = next(it)
    for (x,y) in it:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return x0,y0, x1,y1

def find_impossible_in_row(row, sbs, ranges, partitions, x0, x1, beacons):
    step = partitions['size']
    nearby_sensors = {k:sbs[k] for k in partitions[row//step]}
    num = 0
    for x in range(x0, x1):
        p = (x,row)
        if p not in beacons and any(manhattan(p, s) <= ranges[s] for s in nearby_sensors):
            num += 1
    return num

def find_possible_in_row(row, sbs, ranges, x0, x1, beacons, partitions):
    step = partitions['size']
    nearby_sensors = partitions[row//step]
    x = x0
    while x < x1:
        p = (x,row)
        if p in beacons:
            x += 1
            continue
        sensor = next((s for s in nearby_sensors if manhattan(p, s) <= ranges[s]), None)
        if not sensor:
            return p

        x = sensor[0] + ranges[sensor] - abs(sensor[1]-row) + 1
    return None


def partition_sensors(sensor_ranges, size=10_000):
    partitions = defaultdict(set)
    partitions['size'] = size
    for s,d in sensor_ranges.items():
        x,y = s
        for yy in range((y-d)//size, (y+d)//size+1):
            partitions[yy].add(s)
    return partitions



def main():
    if 'test' in sys.argv[1:]:
        row = 10
        size = 20
        srcfile = 'egdata'
        step = 100
    else:
        row = 2000000
        size = 4000000
        srcfile = 'data'
        step = 10_000
    sbs = read_input(srcfile)
    beacons = set(sbs.values())
    ranges = {p:manhattan(p,b) for (p,b) in sbs.items()}
    print("(partitioning)")
    partitions = partition_sensors(ranges, size=step)
    max_md = max(ranges.values())
    x0,y0, x1,y1 = find_bounds(itertools.chain(sbs, sbs.values()))

    print(f"(finding impossible in row {row})")

    num = find_impossible_in_row(row, sbs, ranges, partitions, x0-max_md, x1+max_md, beacons) # 5838453
    print(f"Num impossible in row {row}: {num}")

    x0=y0=0
    x1=y1=size+1

    for row in range(y0, y1):
        p = find_possible_in_row(row, sbs, ranges, x0, x1, beacons, partitions)
        if p is not None:
            break

    print("Beacon:", p)
    if p is not None:
        print("Frequency:", p[0]*4_000_000 + p[1])


if __name__ == '__main__':
    main()
