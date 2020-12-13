#!/usr/bin/env python3

import sys

def read_input():
    a,b = sys.stdin.read().splitlines()
    return int(a), b.split(',')

def wait_time(start, bus):
    m = start%bus
    return m and bus-m

def hcf(a, b):
    if b < a:
        a,b = b,a
    while a:
        a,b = b%a, a
    return b

def euclid_ext(a, b):
    """Extended Euclidean algorithm:
    finds coefficients of two numbers in order to sum to their highest common factor."""
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1
    r0 = a
    r1 = b
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return s0, t0

def chinese_remainder(time_data):
    """Chinese remainder theorem:
    Finds a number with the given sequence of mods for the given sequence of numbers,
    as long as the sequence of numbers are coprime.
    https://brilliant.org/wiki/chinese-remainder-theorem/"""
    n = 1
    for _,b in time_data:
        n *= b
    y = [n//b for _,b in time_data]
    z = [euclid_ext(yy, td[1])[0] for (yy, td) in zip(y, time_data)]
    return sum(td[0]*yy*zz for (td, yy, zz) in zip(time_data, y, z)) % n

def main():
    start, csv = read_input()
    buses = [int(v) for v in csv if v.isdigit()]
    buses.sort()
    bus_waits = [wait_time(start, bus) for bus in buses]
    min_wait = min(bus_waits)
    i = bus_waits.index(min_wait)
    bus = buses[i]
    print("Part 1:", bus*min_wait)

    time_data =[[i, int(v)] for i,v in enumerate(csv) if v.isdigit()]
    for td in time_data:
        i,b = td
        i %= b
        if i:
            td[0] = b-i

    # Assumption: bus ids are coprime
    t = chinese_remainder(time_data)
    print("Part 2:", t)

if __name__ == '__main__':
    main()
