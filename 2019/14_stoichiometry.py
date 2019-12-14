#!/usr/bin/env python3

import sys
import re
from collections import namedtuple, defaultdict

Component = namedtuple('Component', 'number name')

Component.__str__ = lambda self : f'{self.number} {self.name}'

ORE = 'ORE'
FUEL = 'FUEL'

class Recipe:
    def __init__(self, output, components):
        self.output = output
        self.components = components
    def __repr__(self):
        return f'{self.output} <= {", ".join(map(str, self.components))}'


def parse_reactions(lines):
    ptn = re.compile(r'(\d+)\s+([A-Z]+)')
    for line in lines:
        inp,_,outp = line.strip().partition('=>')
        if not outp:
            continue
        inps = [x.strip() for x in inp.split(',')]
        comps = tuple(Component(int(m.group(1)), m.group(2)) for m in
                         map(ptn.match, inps))
        m = ptn.match(outp.strip())
        num = int(m.group(1))
        name = m.group(2)
        yield Recipe(output=Component(num, name), components=comps)

def ore_needed(reactions, fuel):
    spare = defaultdict(int)
    require = defaultdict(int)
    require[FUEL] = fuel
    ore = 0
    while require:
        name, num_needed = next(iter(require.items()))
        if spare[name] >= num_needed:
            spare[name] -= num_needed
            del require[name]
            continue
        extra_needed = num_needed - spare[name]
        reaction = reactions[name]
        out_num = reaction.output.number
        num_reactions = (extra_needed + out_num - 1) // out_num
        for comp in reaction.components:
            amount_needed = comp.number * num_reactions
            if comp.name==ORE:
                ore += amount_needed
            else:
                require[comp.name] += amount_needed
        produced = out_num * num_reactions
        spare[name] += produced - num_needed
        del require[name]
    return ore

def fuel_search(reactions, ore, least, most):
    while ore_needed(reactions, least) > ore:
        least //= 2
    while ore_needed(reactions, most) <= ore:
        most *= 2
    while least + 1 < most:
        mid = (least + most) // 2
        mid_ore = ore_needed(reactions, mid)
        if mid_ore > ore:
            most = mid
        else:
            least = mid
    return least


def main():
    reactions = {r.output.name: r for r in parse_reactions(sys.stdin)}
    ore_per_fuel = ore_needed(reactions, 1)
    print("Ore needed for one fuel:", ore_per_fuel)

    ore_available = 1_000_000_000_000
    guess = ore_available // ore_per_fuel
    most_fuel = fuel_search(reactions, ore_available, guess, 2*guess)
    print("Amout of fuel from a trillion ore:", most_fuel)

if __name__ == '__main__':
    main()
