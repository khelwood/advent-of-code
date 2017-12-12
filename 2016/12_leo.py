#!/usr/bin/env python3

from collections import defaultdict
import re
import sys

def _compile(x):
    return re.compile('^'+x.replace(' ',r'\s+').replace('#',r'([\w-]+)')+'$')

def _match(ptn, line):
    m = ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    return m

COPY_PTN = _compile('cpy # #')
ALTER_PTN = _compile('(inc|dec) #')
JUMP_PTN = _compile('jnz # #')

def isnum(x):
    return x.startswith('-') or x.isdigit()

class Program:
    def __init__(self, lines):
        self.registers = defaultdict(int)
        self.lines = lines
        self.position = 0
    def __getitem__(self, key):
        if key.isdigit() or key.startswith('-'):
            return int(key)
        return self.registers[key]
    def __setitem__(self, key, value):
        self.registers[key] = int(value)
    def advance(self, amount=1):
        self.position += amount
    def process(self, line):
        if line.startswith('cpy'):
            return self.process_copy(line)
        if line.startswith('inc') or line.startswith('dec'):
            return self.process_update(line)
        if line.startswith('jnz'):
            return self.process_jump(line)
        raise ValueError(repr(line))
    def process_copy(self, line):
        m = _match(COPY_PTN, line)
        src = m.group(1)
        dst = m.group(2)
        if isnum(dst):
            sys.stderr.write("skipping %r"%line)
        else:
            self[dst] = self[src]
        self.advance()
    def process_update(self, line):
        m = _match(ALTER_PTN, line)
        delta = (1 if line.startswith('inc') else -1)
        dst = m.group(2)
        if isnum(dst):
            sys.stderr.write("skipping %r"%line)
        else:
            self[dst] += delta
        self.advance()
    def process_jump(self, line):
        m = _match(JUMP_PTN, line)
        src = m.group(1)
        dst = m.group(2)
        if self[src]:
            if dst.startswith('-') and self.unwrap(src, int(dst)):
                return self.advance()
            self.advance(self[dst])
        else:
            self.advance()
    def unwrap(self, src, delta):
        if delta==-2 and self.unwrap_two(src, self.position-2):
            return True
        return False
    def unwrap_two(self, src, start):
        """If we have a loop of two updates, we can
        compute the outcome without having to run the whole thing."""
        ms = [ALTER_PTN.match(self.lines[start+i]) for i in range(2)]
        if not all(ms):
            return False
        ops = [m.group(1) for m in ms]
        variables = [m.group(2) for m in ms]
        if src not in variables:
            return False
        dst = variables[variables[0]==src]
        if ops[0]==ops[1]:
            self[dst] -= self[src]
        else:
            self[dst] += self[src]
        self[src] = 0
        return True
    def run(self):
        while self.position < len(self.lines):
            self.process(self.lines[self.position])

def main():
    data = sys.stdin.read().strip()
    lines = data.split('\n')
    prog = Program(lines)
    # PART 2:
    prog['c'] = 1
    print("Running...")
    prog.run()
    print(f"prog['a']=={prog['a']}")
            
if __name__ == '__main__':
    main()
