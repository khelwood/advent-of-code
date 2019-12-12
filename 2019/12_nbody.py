#!/usr/bin/env python3

import sys
import re
from itertools import combinations, chain
from functools import reduce

def sign(n):
    return -1 if n<0 else 0 if n==0 else 1

class BodyAxis:
    def __init__(self, pos):
        self.pos = pos
        self.vel = 0
    def advance(self):
        self.pos += vel
    def state(self):
        return (self.pos, self.vel)

def apply_gravity(bodies):
    for alpha, beta in combinations(bodies, 2):
        diff = alpha.pos - beta.pos
        diff = sign(diff)
        beta.vel += diff
        alpha.vel -= diff

def parse_positions(lines):
    pattern = re.compile('<x=#, y=#, z=#>'.replace(' ', r'\s*')
                             .replace('#', '(-?\d+)'))
    for line in lines:
        line = line.strip()
        if line:
            m = re.match(pattern, line)
            if not m:
                raise ValueError("Unparsable line: %r"%line)
            yield tuple(map(int, m.groups()))

def axis_state(bodies, index):
    return tuple(chain.from_iterable((body.pos[index], body.vel[index])
                                         for body in bodies))

def time_step(bodies):
    apply_gravity(bodies)
    for body in bodies:
        body.pos += body.vel

def energy(axis_bodies):
    total_energy = 0
    for body in zip(*axis_bodies):
        ke = sum(abs(ba.pos) for ba in body)
        pe = sum(abs(ba.vel) for ba in body)
        total_energy += ke*pe
    return total_energy

def find_repeat_slow(bodies):
    states = {}
    time = 0
    while True:
        new_state = tuple(chain.from_iterable(body.state() for body in bodies))
        if new_state in states:
            previous = states[new_state]
            return (previous, time-previous)
        states[new_state] = time
        time_step(bodies)
        time += 1

def find_repeat_fast(bodies):
    initial_pos = tuple(body.pos for body in bodies)
    time = 0
    while True:
        time_step(bodies)
        time += 1
        if (all(body.vel==0 for body in bodies) and
               all(body.pos==pos for (body, pos) in zip(bodies, initial_pos))):
            return (0, time)

def hcf(a,b):
    a = abs(a)
    b = abs(b)
    if b < a:
        a,b = b,a
    while a:
        a,b = b%a, a
    return b

def lcm(a, b):
    return a*b // hcf(a,b)

def find_combined_period(repeats):
    if all(start==0 for (start,period) in repeats):
        return reduce(lcm, (period for (start,period) in repeats))

    # This takes a long time (minutes, not years)
    longest_period = 0
    for index, (start, period) in enumerate(repeats):
        if period > longest_period:
            longest_period = period
            longest_index = index
    start,period = repeats[longest_index]
    repeats = [r for (i,r) in enumerate(repeats) if i!=longest_index]
    time = start
    while True:
        time += period
        if all((time-axis_start)%axis_period==0
                   for (axis_start, axis_period) in repeats):
            return time

def main():
    positions = tuple(parse_positions(sys.stdin))
    axis_bodies = [[BodyAxis(pos[i]) for pos in positions] for i in range(3)]
    steps = 1000
    for _ in range(steps):
        for bodies in axis_bodies:
            time_step(bodies)
    print("Energy:", energy(axis_bodies))
    print("(finding periods for each axis)")
    axis_bodies = [[BodyAxis(pos[i]) for pos in positions] for i in range(3)]

    # We're going to assume that all moons return to their initial state,
    # because it makes stuff work faster.
    find_repeat = find_repeat_fast

    repeats = [find_repeat(bodies) for bodies in axis_bodies]
    print("(finding combined period)")
    print("Time:", find_combined_period(repeats))

if __name__ == '__main__':
    main()
