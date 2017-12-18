#!/usr/bin/env python3

import sys
import re

def isnum(name):
    return name.startswith('-') or name.isdigit()

class Command:
    commands = []
    def __init__(self, expr, function):
        self.name = expr
        self.pattern = re.compile('^'+expr.replace('X', r'(-?[0-9]+|\w+)')+'$')
        self.function = function
    def __call__(self, registers, line):
        m = self.pattern.match(line)
        if not m:
            return False
        self.function(registers, *m.groups())
        return True
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Command(%r)"%self.name
    @classmethod
    def run(cls, registers, line):
        if not any(cmd(registers, line) for cmd in cls.commands):
            raise ValueError(repr(line))

def add_command(expr):
    def add_command(fn):
        Command.commands.append(Command(expr, fn))
        return fn
    return add_command

class Registers:
    def __init__(self, single_mode):
        self.data = {}
        self.sound = None
        self.recovered = None
        self.next_line_offset = 1
        self.single_mode = single_mode
        self.send_count = 0
    def __getitem__(self, name):
        return int(name) if isnum(name) else self.data.get(name, 0)
    def __setitem__(self, name, value):
        self.data[name] = value
    def __len__(self):
        return len(self.data)
    @add_command('set X X')
    def set(self, tgt, src):
        self[tgt] = self[src]
    @add_command('snd X')
    def snd(self, src):
        if self.single_mode:
            self.sound = self[src]
        else:
            self.send_count += 1
            self.output_queue.append(self[src])
    @add_command('add X X')
    def add(self, tgt, src):
        self[tgt] += self[src]
    @add_command('mul X X')
    def mul(self, tgt, src):
        self[tgt] *= self[src]
    @add_command('mod X X')
    def mod(self, tgt, src):
        self[tgt] %= self[src]
    @add_command('rcv X')
    def rcv(self, var):
        if self.single_mode:
            if self[var]:
                self.recovered = self.sound
                self.sound = None
        else:
            if self.input_queue:
                self[var] = self.input_queue.pop(0)
            else:
                self.next_line_offset = 0
    @add_command('jgz X X')
    def jgz(self, src, delta):
        if self[src] > 0:
            self.next_line_offset = self[delta]

def run_single(prog, lines):
    position = 0
    while 0 <= position < len(lines):
        prog.next_line_offset = 1
        Command.run(prog, lines[position])
        position += prog.next_line_offset
        if prog.recovered:
            return prog.recovered

def run_coop(programs, lines):
    positions = [0,0]
    deadlock_detector = 0
    while all(0 <= pos < len(lines) for pos in positions):
        for i in range(2):
            prog = programs[i]
            prog.next_line_offset = 1
            line = lines[positions[i]]
            Command.run(prog, line)
            if prog.next_line_offset:
                positions[i] += prog.next_line_offset
                deadlock_detector = 0
            else:
                deadlock_detector += 1
                if deadlock_detector > len(programs):
                    print("(deadlock)")
                    return

def main():
    lines = sys.stdin.read().strip().split('\n')
    prog = Registers(True)
    print("One program:")
    print(' ...', end='\r')
    recovered = run_single(prog, lines)
    print("Recovered:", recovered)
    programs = [Registers(False), Registers(False)]
    for i in range(2):
        prog = programs[i]
        prog.output_queue = programs[1-i].input_queue = []
        prog['p'] = i
    print("Two programs:")
    print(' ...', end='\r')
    send_counts = run_coop(programs, lines)
    print("Sent:", programs[1].send_count)

if __name__ == '__main__':
    main()
