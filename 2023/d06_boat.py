#!/usr/bin/env python3

import sys
import re
import math

# Race has length D and allowed time T.
# Hold the button for time H.
# Boat then moves at speed H for (T-H).
# It travels distance H*(T-H) in the allowed time.
# It reaches distance D at time H + D/H.

# Suppose H*(T-H) = D
#  H*(H-T) = -D
#  H² - TH + D = 0
#  H = (T ± sqrt(T² - 4D))/2

NUM_PTN = re.compile(r'\d+')

def read_races(lines):
    line1, line2 = lines
    assert line1.startswith('Time:')
    assert line2.startswith('Distance:')
    times = map(int, NUM_PTN.findall(line1))
    distances = map(int, NUM_PTN.findall(line2))
    return list(zip(times, distances))

def min_hold_time(t, d):
    h = math.ceil((t - math.sqrt(t*t - 4*d)) / 2)
    if h*(t-h) <= d:
        h += 1
    return h

def max_hold_time(t, d):
    h = math.floor((t + math.sqrt(t*t - 4*d)) / 2)
    if h*(t-h) <= d:
        h -= 1
    return h

def read_big_race(lines):
    line1, line2 = lines
    time = int(''.join(NUM_PTN.findall(line1)))
    distance = int(''.join(NUM_PTN.findall(line2)))
    return time, distance

def main():
    lines = sys.stdin.read().strip().splitlines()
    races = read_races(lines)
    prod = 1
    for (t,d) in races:
        num_solutions = 1 + max_hold_time(t,d) - min_hold_time(t,d)
        prod *= num_solutions
    print("Part 1:", prod)
    t,d = read_big_race(lines)
    num_solutions = 1 + max_hold_time(t,d) - min_hold_time(t,d)
    print("Part 2:", num_solutions)

if __name__ == '__main__':
    main()
