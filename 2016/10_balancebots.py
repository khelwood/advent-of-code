#!/usr/bin/env python3

import sys
import re

# The queue of bots that need to pass on chips to their pals.
# These are queued up as chips are passed around so that the
# exchanges happen in a reasonable order.

check_queue = []

class Bot:
    is_bot = True
    def __init__(self, name):
        self.name = name
        self.high_to = None
        self.low_to = None
        self.chips = []
        self.comparisons = []
    def receive(self, chip):
        self.chips.append(chip)
        if len(self.chips) > 1:
            check_queue.append(self)
    def check_capacity(self):
        if len(self.chips) > 1:
            self.dispense()
    def dispense(self):
        self.chips.sort()
        l,h = self.chips
        self.comparisons.append((l,h))
        self.chips = []
        self.low_to.receive(l)
        self.high_to.receive(h)

class Output:
    is_bot = False
    def __init__(self, name):
        self.name = name
        self.chips = []
    def receive(self, chip):
        self.chips.append(chip)

class BotDict(dict):
    def __missing__(self, key):
        v = Bot(key) if key.startswith('bot') else Output(key)
        self[key] = v
        return v

agents = BotDict()

def _compile(expr):
    return re.compile(expr.replace('BOT', '(\w+ [0-9]+)'))

def _match(ptn, line):
    m = re.match(ptn, line)
    if not m:
        raise ValueError(repr(line))
    return m

BOT_PTN = _compile('BOT gives low to BOT and high to BOT')
INPUT_PTN = _compile('value ([0-9]+) goes to BOT')

def process_bot(line):
    m = _match(BOT_PTN, line)
    donor, low, high = [agents[m.group(i)] for i in range(1,4)]
    donor.low_to = low
    donor.high_to = high

def process_input(line):
    m = _match(INPUT_PTN, line)
    v = int(m.group(1))
    bot = agents[m.group(2)]
    bot.receive(v)
    while check_queue:
        check_queue.pop(0).check_capacity()

def process_lines(lines):
    input_lines = []
    for line in lines:
        if line.startswith('bot'):
            process_bot(line)
        else:
            input_lines.append(line)
    for line in input_lines:
        process_input(line)

def main():
    lines = sys.stdin.read().strip().split('\n')
    process_lines(lines)
    for agent in agents.values():
        if agent.is_bot and (17, 61) in agent.comparisons:
            print(f'{agent.name} compared 17 and 61.')
    a,b,c = [agents[f'output {i}'].chips[0] for i in range(3)]
    print("Product:", a*b*c)

if __name__ == '__main__':
    main()
