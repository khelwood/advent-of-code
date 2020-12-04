#!/usr/bin/env python3

"""
Droid will say "Command?"
I will issue a command ending in a newline (ASCII 10).
Commands:
"north", "south", "east", "west"
"take <item>"
"drop <item>"
"inv"
"""

import sys
import re
from intcode import Program, parse_program_input

TAKEDROP = re.compile('^(take|drop)( \w+)+$')
SIMPLE_COMMANDS = {'north', 'south', 'east', 'west', 'inv'}

def read_command():
    print()
    while True:
        s = input('> ').lower().strip()
        if len(s)==1:
            c = next((w for w in SIMPLE_COMMANDS if w[0]==s), None)
            if c:
                return c+'\n'
        if s in SIMPLE_COMMANDS:
            return s+'\n'
        if re.match(TAKEDROP, s):
            return s+'\n'
        print('???')

def droid_input(buffer=[]):
    if buffer:
        return buffer.pop(0)
    cmd = read_command()
    buffer.extend(map(ord, cmd))
    return buffer.pop(0)

def droid_output(value):
    print(chr(value), end='', flush=True)
        
def main():
    filename = 'savedata'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename, 'r') as fin:
        data = fin.read()
    program_input = parse_program_input(data)
    droid = Program(program_input)
    droid.input_func = droid_input
    droid.output_func = droid_output
    droid.execute()

if __name__ == '__main__':
    main()
# Tambourine is too heavy
# Loom is too heavy
