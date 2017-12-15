#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

def isnum(name):
    return name.startswith('-') or name.isdigit()

class WireValues:
    def __init__(self):
        self.wires = {}
    def __getitem__(self, name):
        return int(name) if isnum(name) else self.wires[name]
    def __setitem__(self, name, value):
        self.wires[name] = value
    def __contains__(self, name):
        return isnum(name) or name in self.wires

Command = namedtuple('Command', 'pattern function')
WireLink = namedtuple('WireLink', 'command inputs output')

COMMANDS = []

def make_command(expr):
    pattern = re.compile('^'+expr.replace('#', '([0-9a-z]+)')+'$')
    def command_maker(function):
        command = Command(pattern, function)
        COMMANDS.append(command)
        return command
    return command_maker

@make_command('# -> #')
def assignment(wires, v1, name):
    wires[name] = wires[v1]

@make_command('# AND # -> #')
def anding(wires, v1, v2, name):
    wires[name] = wires[v1] & wires[v2]

@make_command('# OR # -> #')
def oring(wires, v1, v2, name):
    wires[name] = wires[v1] | wires[v2]

@make_command('# LSHIFT # -> #')
def lshift(wires, v1, v2, name):
    wires[name] = wires[v1] << wires[v2]

@make_command('# RSHIFT # -> #')
def rshift(wires, v1, v2, name):
    wires[name] = wires[v1] >> wires[v2]

@make_command('NOT # -> #')
def notting(wires, v1, name):
    wires[name] = ((1<<16)-1)&~wires[v1]

def create_link(line):
    for cmd in COMMANDS:
        m = re.match(cmd.pattern, line)
        if m:
            gps = m.groups()
            return WireLink(cmd, gps[:-1], gps[-1])
    raise ValueError(repr(line))

def process_links(links):
    wires = WireValues()
    while links:
        remaining = []
        for link in links:
            if all(i in wires for i in link.inputs):
                link.command.function(wires, *link.inputs, link.output)
            else:
                remaining.append(link)
        links = remaining
    return wires

def main():
    lines = sys.stdin.read().strip().split('\n')
    links = [create_link(line) for line in lines]
    wires = process_links(links)
    answer = wires['a']
    print("Part 1 wire a:", answer)
    index = next(i for (i,link) in enumerate(links) if link.output=='b')
    links[index] = WireLink(assignment, [str(answer)], 'b')
    wires = process_links(links)
    answer = wires['a']
    print("Part 2 wire a:", answer)

if __name__ == '__main__':
    main()
