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

def routes_from(pos, dists, remaining, mins):
    for dest in remaining:
        newmins = mins - dists[pos,dest] - 1
        if newmins >= 0:
            found = False
            for new in routes_from(dest, dists, remaining-{dest}, newmins):
                found = True
                route = (dest,) + new
                yield route
            yield (dest,)

def calculate_flow(route, dists, flows, mins, cache):
    if route in cache:
        return cache[route]
    pos = 'AA'
    flow = 0
    for new in route:
        d = dists[pos,new]
        mins -= d + 1
        flow += flows[new]*mins
        pos = new
    cache[route] = flow
    return flow

def elephant_flow(dists, flows, remaining, mins, cache, flowcache):
    r = cache.get(remaining)
    if r is not None:
        return r
    best_flow = 0
    for e in routes_from('AA', dists, remaining, mins):
        flow = calculate_flow(e, dists, flows, mins, flowcache)
        if flow > best_flow:
            best_flow = flow
    cache[remaining] = best_flow
    return best_flow


def main():
    exits, flows = read_valves(sys.stdin)
    dists = find_distances(exits)
    c = 0
    best_route = None
    best_flow = 0
    remaining = frozenset(k for (k,v) in flows.items() if v)
    mins = 30
    flowcache = {}
    for r in routes_from('AA', dists, remaining, mins):
        flow = calculate_flow(r, dists, flows, mins, flowcache)
        if flow > best_flow:
            best_flow = flow
            best_route = r
    print(best_route)
    print(best_flow)
    mins = 26
    best_flow = 0
    num_routes = 0
    cache = {}
    flowcache = {}
    for r in routes_from('AA', dists, remaining, mins):
        myflow = calculate_flow(r, dists, flows, mins, flowcache)
        eleflow = elephant_flow(dists, flows, remaining.difference(r), mins,
            cache, flowcache)
        total = myflow + eleflow
        if total > best_flow:
            best_flow = total
        num_routes += 1
        if num_routes%1000==0:
            print(f' [{num_routes}]',end='\r')
    print()
    print(best_flow)


if __name__ == '__main__':
    main()
