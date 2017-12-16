#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Reindeer = namedtuple('Reindeer', 'name speed duration rest')

REINDEER_PTN = re.compile(r'^(\w+) can fly # km/s for # seconds?, but then '
                            'must rest for # seconds?.$'
                            .replace('#', '([0-9]+)'))

def load_team(lines):
    team = []
    for line in lines:
        m = re.match(REINDEER_PTN, line)
        if not m:
            raise ValueError(repr(line))
        name = m.group(1)
        vals = [int(m.group(i)) for i in range(2,5)]
        team.append(Reindeer(name, *vals))
    return team

def run_distance(reindeer, time):
    cycle_time = reindeer.duration + reindeer.rest
    cycle_distance = reindeer.duration * reindeer.speed
    cycles = time//cycle_time
    after_cycle = time%cycle_time
    return (cycle_distance * cycles
            + min(cycle_distance, reindeer.speed * after_cycle))

def score_winners(team, time):
    scores = [0] * len(team)
    for t in range(1, time+1):
        distances = [run_distance(reindeer, t) for reindeer in team]
        furthest = max(distances)
        for i,distance in enumerate(distances):
            if distance==furthest:
                scores[i] += 1
    return scores

def main():
    time = 2503
    if len(sys.argv) > 1:
        time = int(sys.argv[1])
    lines = sys.stdin.read().strip().split('\n')
    team = load_team(lines)
    longest = max(run_distance(reindeer, time) for reindeer in team)
    print("Longest distance:", longest)
    scores = score_winners(team, time)
    print("Greatest score:", max(scores))
    

if __name__ == '__main__':
    main()
