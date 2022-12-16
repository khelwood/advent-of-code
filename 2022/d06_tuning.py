#!/usr/bin/env python3

import sys
from collections import Counter

def find_packet_start(data, target=4):
    c = Counter(data[:target])
    count = len(c)
    if count==target:
        return target
    for i in range(target, len(data)):
        old = data[i-target]
        new = data[i]
        v = c[old]
        if v==1:
            count -= 1
        c[old] = v-1
        v = c[new]
        if v==0:
            count += 1
        c[new] = v+1
        if count==target:
            return i+1
    return -1

def main():
    data = sys.stdin.read().strip()
    n = find_packet_start(data)
    print("Packet start:", n)
    n = find_packet_start(data, 14)
    print("Message start:", n)

if __name__ == '__main__':
    main()
