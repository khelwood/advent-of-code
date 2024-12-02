#!/usr/bin/env python3

import sys
from collections import Counter

def read_data():
    data = ([],[])
    for line in filter(bool, map(str.strip, sys.stdin)):
        a,b = map(int, line.split())
        data[0].append(a)
        data[1].append(b)
    return data

def list_distance(data):
    la, lb = map(sorted, data)
    return sum(abs(a-b) for (a,b) in zip(la,lb))

def list_similarity(data):
    la, lb = data
    bc = Counter(lb)
    return sum(a*bc[a] for a in la)


def main():
    data = read_data()
    print(list_distance(data))
    print(list_similarity(data))

if __name__ == '__main__':
    main()
