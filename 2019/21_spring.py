#!/usr/bin/env python3

import sys
from intcode import Program, parse_program_input

WALK_PROG = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
'''

RUN_PROG = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND E T
OR H T
AND T J
RUN
'''

def rindex(seq, value):
    for i in range(len(seq)-1, -1, -1):
        if seq[i]==value:
            return i
    raise ValueError('Value not found in sequence')

def run_droid(prog_input, droid_input):
    prog = Program(prog_input)
    prog.run_input(droid_input)
    last = rindex(prog.output_values, ord('\n')) + 1
    print(''.join(map(chr, prog.output_values[:last])))
    print(prog.output_values[last:])

def main():
    prog_input = parse_program_input(sys.stdin.read().strip())
    run_droid(prog_input, WALK_PROG)
    run_droid(prog_input, RUN_PROG)

if __name__ == '__main__':
    main()
