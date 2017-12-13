import sys
import re
from collections import namedtuple, defaultdict

def isnum(x):
    return x.startswith('-') or x.isdigit()

def compile(exp):
    return re.compile('^'+exp.replace(' ',r'\s+').replace('#',r'([\w-]+)')+'$')

Command = namedtuple('Command', 'pattern function')

class Program:
    def __init__(self, lines):
        self.registers = defaultdict(int)
        self.lines = lines
        self.position = 0
        self.commands = []
        self.unwrappers = []
        self.toggles = []
        self.verbose = False
    def add_command(self, ptn, fn):
        self.commands.append(Command(ptn, fn))
    def add_unwrapper(self, fn):
        self.unwrappers.append(fn)
    def add_toggle(self, old, new):
        self.toggles.append((old, new))
    def __getitem__(self, key):
        if key.isdigit() or key.startswith('-'):
            return int(key)
        return self.registers[key]
    def __setitem__(self, key, value):
        self.registers[key] = int(value)
    def advance(self, amount=1):
        self.position += amount
    def process(self, line):
        if self.verbose:
            print(" %s  "%self.position, end='\r')
        for command in self.commands:
            match = re.match(command.pattern, line)
            if match:
                return command.function(self, line, match)
        raise ValueError(repr(line))
    def unwrap(self, line, src, delta):
        return any(uw(self, line, src, delta) for uw in self.unwrappers)
    def toggle(self, line):
        for old, new in self.toggles:
            if line.startswith(old):
                return new + line[len(old):]
        return line
    def run(self):
        while self.position < len(self.lines):
            self.process(self.lines[self.position])

# ------
# Puzzle 12
# ------
            
COPY_PTN = compile('cpy # #')
ALTER_PTN = compile('(inc|dec) #')
JUMP_PTN = compile('jnz # #')

def process_copy(prog, line, match):
    src = match.group(1)
    dst = match.group(2)
    if isnum(dst):
        print("(skipping %r)"%line)
    else:
        prog[dst] = prog[src]
    prog.advance()

def process_update(prog, line, match):
    delta = (1 if line.startswith('inc') else -1)
    dst = match.group(2)
    if isnum(dst):
        print("(skipping %r)"%line)
    else:
        prog[dst] += delta
    prog.advance()

def process_jump(prog, line, match):
    src = match.group(1)
    dst = match.group(2)
    if prog[src]:
        if dst.startswith('-') and prog.unwrap(line, src, int(dst)):
            return prog.advance()
        prog.advance(prog[dst])
    else:
        prog.advance()

def unwrap_two(prog, line, src, delta):
    if delta!=-2:
        return False
    start = prog.position + delta
    ms = [ALTER_PTN.match(prog.lines[start+i]) for i in range(2)]
    if not all(ms):
        return False
    ops = [m.group(1) for m in ms]
    variables = [m.group(2) for m in ms]
    if src not in variables:
        return False
    dst = variables[variables[0]==src]
    if ops[0]==ops[1]:
        prog[dst] -= prog[src]
    else:
        prog[dst] += prog[src]
    prog[src] = 0
    if prog.verbose:
        print("(unwrapping %r)"%line)
    return True

# ---------
# Puzzle 23
# ---------

TOGGLE_PTN = compile('tgl #')

def process_toggle(prog, line, match):
    arg = match.group(1)
    index = prog.position + prog[arg]
    if 0 <= index < len(prog.lines):
        old_line = prog.lines[index]
        new_line = prog.toggle(old_line)
        if prog.verbose:
            print("Toggle %r -> %r"%(old_line, new_line))
        prog.lines[index] = new_line
    prog.advance()

def unwrap_five(prog, line, src, delta):
    """The described pattern of 5 lines then a jump backwards
    amounts to a multiplication using nested for loops."""
    if delta!=-5:
        return False
    start = prog.position - 5
    lines = prog.lines[start:start+5]
    patterns = [COPY_PTN, ALTER_PTN, ALTER_PTN, JUMP_PTN, ALTER_PTN]
    matches = [re.match(p,line) for (p,line) in zip(patterns, lines)]
    if not all(matches):
        return False
    src_0 = matches[0].group(1)
    dst_0 = matches[0].group(2)
    delta = 1 if matches[1].group(1)=='inc' else -1
    obj_1 = matches[1].group(2)
    obj_2 = matches[2].group(2)
    test_3 = matches[3].group(1)
    delta_3 = matches[3].group(2)
    obj_4 = matches[4].group(2)
    if not (dst_0==obj_2==test_3 and prog[delta_3]==-2
            and len({src_0, dst_0, obj_1, obj_4, delta_3})==5):
        return False
    prog[obj_1] += delta * prog[src_0] * prog[obj_4]
    prog[obj_4] = 0
    prog[obj_2] = 0
    if prog.verbose:
        print("(unwrapping %r)"%line)
    return True

# ---------
# Puzzle 25
# ---------

OUT_PTN = compile('out #')

OUT_LIMIT = 100

class OutputResult(Exception):
    pass

class OutputSuccess(OutputResult):
    pass

class OutputError(OutputResult):
    pass

def process_out(prog, line, match):
    obj = match.group(1)
    value = prog[obj]
    if prog.verbose:
        print("OUT", value)
    if value != prog.out_count%2:
        raise OutputError()
    prog.out_count += 1
    if prog.out_count >= OUT_LIMIT:
        raise OutputSuccess()
    prog.advance()

# ---------------
# Program factory
# ---------------

def make_program(lines, toggles=False, outs=False):
    prog = Program(lines)
    prog.add_command(COPY_PTN, process_copy)
    prog.add_command(ALTER_PTN, process_update)
    prog.add_command(JUMP_PTN, process_jump)
    prog.add_unwrapper(unwrap_two)
    if toggles:
        prog.add_command(TOGGLE_PTN, process_toggle)
        prog.add_unwrapper(unwrap_five)
        prog.add_toggle('inc', 'dec')
        prog.add_toggle('dec', 'inc')
        prog.add_toggle('tgl', 'inc')
        prog.add_toggle('jnz', 'cpy')
        prog.add_toggle('cpy', 'jnz')
    if outs:
        prog.add_command(OUT_PTN, process_out)
        prog.add_toggle('out', 'inc')
        prog.last_out = None
        prog.out_count = 0
    return prog
