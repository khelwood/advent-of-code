#!/usr/bin/env python3

import sys
import re
from typing import NamedTuple

BLUEPRINT_PTN = re.compile(r'''
Blueprint %:\s*Each ore robot costs % ore.
Each clay robot costs % ore.
Each obsidian robot costs % ore and % clay.
Each geode robot costs % ore and % obsidian.
'''.strip()
   .replace('%', r'(\d+)')
   .replace('\n', r'\s*')
   .replace('.', r'\.'),
re.M)

ORE = 0
CLAY = 1
OBS = 2
GEODE = 3

RESOURCE_NAMES = 'ore clay obsidian geode'.split()
RES_RANGE = range(len(RESOURCE_NAMES))

class Resources(tuple):
    def __add__(self, other):
        return Resources(a+b for a,b in zip(self, other))

    def __sub__(self, other):
        return Resources(a-b for a,b in zip(self, other))

    def inc(self, name, diff=1):
        return Resources(a+ (diff if name==i else 0)
                        for (i,a) in enumerate(self))

    @classmethod
    def from_dict(cls, dct):
        return cls(dct.get(k, 0) for k in RESOURCE_NAMES)

    def __repr__(self):
        return '{' + ', '.join(f'{k}:{v}' for (k,v) in zip(RESOURCE_NAMES,self)) + '}'

class Costs(tuple):
    def __init__(self, *args):
        self.max = self._calculate_max()

    def _calculate_max(self):
        return tuple(max(cost[r] for cost in self) for r in RES_RANGE)

    @classmethod
    def from_dict(cls, all_costs):
        return cls(Resources.from_dict(all_costs[k]) for k in RESOURCE_NAMES)

class Blueprint(NamedTuple):
    index: int
    costs: Costs

def parse_blueprints(data):
    for m in BLUEPRINT_PTN.finditer(data):
        gps = list(map(int, m.groups()))
        #bi, oreore, clayore, obore, obclay, geore, geob
        costs = {
            'ore': {'ore':gps[1]},
            'clay': {'ore':gps[2]},
            'obsidian': {'ore':gps[3], 'clay':gps[4]},
            'geode': {'ore':gps[5], 'obsidian':gps[6]},
        }
        yield Blueprint(gps[0], Costs.from_dict(costs))

def can_wait_for(robcost, robots):
    return all(c==0 or robots[i] for (i,c) in enumerate(robcost))

def useful(costs, robot, robots, turns):
    if turns==0:
        return False
    if robot==GEODE:
        return True
    return robots[robot] < costs.max[robot]

def next_robot(costs, robots, resources, turns):
    can_build = False
    can_wait = False
    for rob, robcost in enumerate(costs):
        if not useful(costs, rob, robots, turns):
            continue
        if all(cos <= resources[res] for (res,cos) in enumerate(robcost)):
            yield rob
            can_build = True
        elif not can_wait:
            can_wait = can_wait_for(robcost, robots)
    if not can_build or can_wait:
        yield -1

def inferior(a,b):
    return all(aa <= bb for (aa,bb) in zip(a,b))

def sort_and_prune(states):
    states = sorted(states, reverse=True)
    i = 1
    while i < len(states):
        res, rob = states[i]
        if any(inferior(res, jres) and inferior(rob, jrob)
                for jres, jrob in (states[j] for j in range(i))):
            del states[i]
        else:
            i += 1
    return states

def track_production(costs, resources, robots, turns):
    new_states = [(resources, robots)]
    turn_states = [[] for _ in range(turns)]
    for time_left in range(turns-1, -1, -1):
        old_states = sort_and_prune(new_states)
        for resources, robots in old_states:
            for robot,robcost in enumerate(costs):
                if not useful(costs, robot, robots, turns):
        for resources, robots in old_states:
            new_resources = resources + robots
            for new_robot in next_robot(costs, robots, resources, time_left):
                if new_robot>=0:
                    ns_resources = new_resources - costs[new_robot]
                    ns_robots = robots.inc(new_robot)
                    new_states.append((ns_resources, ns_robots))
                else:
                    new_states.append((new_resources, robots))
        print(time_left, len(new_states))
    return max(res[GEODE] for res,_ in new_states)

def main():
    blueprints = list(parse_blueprints(sys.stdin.read().strip()))
    initial_resources = Resources((0,)*len(RESOURCE_NAMES))
    initial_robots = Resources(int(k==ORE) for k in RES_RANGE)
    total = 0
    for b in blueprints:
        score = track_production(b.costs, initial_resources, initial_robots, 24)
        total += score * b.index
        print(b.index, score)
    print("Part 1:", total)
    total = 1
    for b in blueprints[:3]:
        score = track_production(b.costs, initial_resources, initial_robots, 32)
        total *= score
        print(b.index, score)
    print("Part 2:", total)
    # IDEA: instead of picking what to do this turn,
    #  add a state to some future for each robot you might build

if __name__ == '__main__':
    main()
