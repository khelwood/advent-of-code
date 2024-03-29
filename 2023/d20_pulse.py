#!/usr/bin/env python3

import sys
import re
import math

from collections import deque, defaultdict

MODULE_PTN = re.compile(r'([%&]?)(\w+) -> (.+)')

LOW = 0
HIGH = 1

class Module:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    def send(self, pulse, queue):
        for v in self.outputs:
            queue.append((v, self.name, pulse))

class Broadcaster(Module):
    def receive(self, source, pulse, queue):
        self.send(pulse, queue)

class FlipFlop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.pulse = LOW

    def receive(self, source, pulse, queue):
        if pulse==LOW:
            self.pulse = 1 - self.pulse
            self.send(self.pulse, queue)

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.inputs = {}

    def receive(self, source, pulse, queue):
        self.inputs[source] = pulse
        out = LOW if all(v==HIGH for v in self.inputs.values()) else HIGH
        self.send(out, queue)


def parse_module(line):
    m = MODULE_PTN.match(line)
    if not m:
        raise ValueError(repr(line))
    name = m.group(2)
    outputs = m.group(3).strip().replace(',',' ').split()
    if name=='broadcaster':
        return Broadcaster(name, outputs)
    if m.group(1)=='%':
        return FlipFlop(name, outputs)
    return Conjunction(name, outputs)

def update_conjunctions(modules):
    sources = defaultdict(set)
    for module in modules.values():
        for out in module.outputs:
            sources[out].add(module.name)
    for module in modules.values():
        if isinstance(module, Conjunction):
            for source in sources[module.name]:
                module.inputs[source] = LOW

def parse_modules(lines):
    modules = {m.name:m for m in map(parse_module, lines)}
    update_conjunctions(modules)
    return modules

def main():
    lines = sys.stdin.read().strip().splitlines()
    modules = parse_modules(lines)
    queue = deque()
    pulse_count = {LOW:0, HIGH:0}
    for _ in range(1000):
        queue.append(('broadcaster', 'button', LOW))
        while queue:
            (name, source, pulse) = queue.popleft()
            pulse_count[pulse] += 1
            if name in modules:
                modules[name].receive(source, pulse, queue)
    pulse_total = pulse_count[LOW]*pulse_count[HIGH]
    print("Part 1:", pulse_total)

    modules = parse_modules(lines)
    conj, = [m for m in modules.values() if 'rx' in m.outputs]
    assert isinstance(conj, Conjunction)
    to_conj = set(conj.inputs)
    n = 0
    queue = deque()
    hits = defaultdict(list)
    enough = False
    while not enough:
        n += 1
        queue.append(('broadcaster', 'button', LOW))
        while queue:
            (name, source, pulse) = queue.popleft()
            if name==conj.name and pulse==HIGH:
                hits[source].append(n)
                if all(len(hits[k]) > 3 for k in to_conj):
                    enough = True
            if name in modules:
                modules[name].receive(source, pulse, queue)
    for k,vs in hits.items():
        delta = vs[1]-vs[0]
        n = 0
        for v in vs:
            n += delta
            assert v==n
        # hits each refers to a linear sequence
        hits[k] = delta
    result = math.lcm(*hits.values())
    print("Part 2:", result)

if __name__ == '__main__':
    main()
