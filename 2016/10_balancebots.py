#!/usr/bin/env python3

import clip
import sys
import re

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
        if key.startswith('bot'):
            v = Bot(key)
        else:
            v = Output(key)
        self[key] = v
        return v

agents = BotDict()

BOT_PTN = re.compile('BOT gives low to BOT and high to BOT'
                         .replace('BOT', '(\w+ [0-9]+)'))
INPUT_PTN = re.compile('value ([0-9]+) goes to (\w+ [0-9]+)')

def process_bot(line):
    m = re.match(BOT_PTN, line)
    if not m:
        raise ValueError(line)
    donor, low, high = [agents[m.group(i)] for i in range(1,4)]
    donor.low_to = low
    donor.high_to = high

def process_input(line):
    m = re.match(INPUT_PTN, line)
    if not m:
        raise ValueError(line)
    v = int(m.group(1))
    bot = agents[m.group(2)]
    bot.receive(v)
    while check_queue:
        check_queue.pop(0).check_capacity()

def process_lines(lines):
    bot_lines = []
    input_lines = []
    for line in lines:
        (bot_lines if line.startswith('bot') else input_lines).append(line)
    for line in bot_lines:
        process_bot(line)
    for line in input_lines:
        process_input(line)

def main():
    if len(sys.argv) > 1:
        x = ' '.join(sys.argv[1:])
    else:
        print("Press enter to paste.")
        input()
        x = clip.paste()
    x = x.strip()
    process_lines(x.split('\n'))
    print("Processed.")
    for agent in agents.values():
        if agent.is_bot and (17, 61) in agent.comparisons:
            print(f'{agent.name} compared 17 and 61.')
    product = 1
    for i in range(3):
        output = agents[f'output {i}']
        print(f"{output.name}: {output.chips}")
        product *= output.chips[0]
    print(f"Product: {product}")

if __name__ == '__main__':
    main()
