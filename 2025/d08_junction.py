#!/usr/bin/env python3

import sys
from itertools import combinations

def d2(a,b):
    ax,ay,az = a
    bx,by,bz = b
    return ((ax-bx)**2 + (ay-by)**2 + (az-bz)**2)

def read_input():
    coords = []
    for line in filter(bool, map(str.strip, sys.stdin)):
        coords.append(tuple(map(int, line.split(','))))
    return coords

def find_distances(jbs):
    dists = {}
    for a,b in combinations(jbs, 2):
        dists[a,b] = d2(a,b)
    return dists

def iter_connections(dists):
    rdist = {}
    for k,v in dists.items():
        if v in rdist:
            rdist[v].append(k)
        else:
            rdist[v] = [k]
    dsort = sorted(rdist)
    for d in dsort:
        pairs = rdist[d]
        for p in pairs:
            yield p

def find_circuits(cnxs, initial=None):
    circuits = initial or {}
    for a,b in cnxs:
        ca = circuits.get(a)
        cb = circuits.get(b)
        if ca and cb:
            ca.update(cb)
            for p in cb:
                circuits[p] = ca
        elif ca:
            circuits[b] = ca
            ca.add(b)
        elif cb:
            circuits[a] = cb
            cb.add(a)
        else:
            circuits[a] = circuits[b] = {a,b}
    return circuits

def circuits_complete(circuits, num):
    return len(next(iter(circuits.values())))==num

def main():
    jbs = read_input()
    num_jbs = len(jbs)
    limit = 10 if num_jbs <= 20 else 1000
    dists = find_distances(jbs)
    it_cnx = iter_connections(dists)
    cnxs = set()
    for _ in range(limit):
        cnxs.add(next(it_cnx))
    circuits = find_circuits(cnxs)
    circuit_set = {frozenset(s) for s in circuits.values()}
    a,b,c,*_ = sorted(circuit_set, key=len, reverse=True)
    print(len(a)*len(b)*len(c))
    while not circuits_complete(circuits, num_jbs):
        cnx = next(it_cnx)
        cnxs.add(cnx)
        circuits = find_circuits((cnx,), circuits)
    a,b = cnx
    print(a[0]*b[0])

if __name__ == '__main__':
    main()
