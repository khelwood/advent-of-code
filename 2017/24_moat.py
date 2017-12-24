#!/usr/bin/env python3

import sys

from collections import namedtuple

State = namedtuple('State', 'strength end remaining')

def strongest(comps):
    states = [State(0, 0, comps)]
    seen = set(states)
    while states:
        next_states = []
        for state in states:
            strength, end, remaining = state
            for i,comp in enumerate(remaining):
                if end not in comp:
                    continue
                new_end = comp[1-(comp[1]==end)]
                ns = State(strength + comp[0]+comp[1], new_end,
                               remaining[:i] + remaining[i+1:])
                if ns in seen:
                    continue
                next_states.append(ns)
                seen.add(ns)
        last_states = states
        states = next_states
    return (max(state.strength for state in seen),
            max(state.strength for state in last_states))

def main():
    lines = sys.stdin.read().strip().split('\n')
    comps = tuple(tuple(map(int, line.split('/'))) for line in lines)
    result = strongest(comps)
    print("Strongest:", result[0])
    print("Strongest longest:", result[1])

if __name__ == '__main__':
    main()
