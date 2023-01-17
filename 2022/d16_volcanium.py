#!/usr/bin/env python3

import sys
import re

def read_valves(fin):
    ptn = re.compile(r'Valve (\w+) has flow rate=(\d+);'
        r' tunnels? leads? to valves? (.*)$')
    flows = {}
    exits = {}
    for line in filter(bool, map(str.strip, fin)):
        m = ptn.match(line)
        if not m:
            raise ValueError('Bad input: %r'%line)
        name = m.group(1)
        flows[name] = int(m.group(2))
        exits[name] = tuple(map(str.strip, m.group(3).split(',')))
    return exits, flows

def find_distances(exits):
    dists = {(k,k):0 for k in exits}
    for pos, outs in exits.items():
        for out in outs:
            dists[pos, out] = 1
    more = True
    while more:
        more = False
        for (x,y) in list(dists):
            newdist = dists[x,y] + 1
            outs = exits[y]
            for z in outs:
                key = (x,z)
                if dists.get(key, newdist+1) > newdist:
                    more = True
                    dists[key] = newdist
                    dists[z,x] = newdist
    return dists

def routes_from(pos, dists, remaining, mins=30):
    for dest in remaining:
        newmins = mins - dists[pos,dest] - 1
        if newmins >= 0:
            found = False
            for new in routes_from(dest, dists, remaining-{dest}, newmins):
                found = True
                route = (dest,) + new
                yield route
            if not found:
                yield (dest,)

def calculate_flow(route, dists, flows):
    mins = 30
    pos = 'AA'
    flow = 0
    for new in route:
        d = dists[pos,new]
        mins -= d + 1
        flow += flows[new]*mins
        pos = new
    return flow

def main():
    exits, flows = read_valves(sys.stdin)
    dists = find_distances(exits)
    c = 0
    best_route = None
    best_flow = 0
    remaining = {k for (k,v) in flows.items() if v}
    for r in routes_from('AA', dists, remaining):
        flow = calculate_flow(r, dists, flows)
        if flow > best_flow:
            best_flow = flow
            best_route = r
    print(best_route)
    print(best_flow)

if __name__ == '__main__':
    main()
