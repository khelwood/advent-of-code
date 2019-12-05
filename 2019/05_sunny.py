#!/usr/bin/env python3

import sys

from program import Program, parse_program_input

def main():
    data = parse_program_input(sys.stdin.read())
    prog = Program(data, [1])
    prog.execute()
    print("First program output:", prog.output[-1])
    prog = Program(data, [5])
    prog.execute()
    print("Second program output:", prog.output[-1])

if __name__ == '__main__':
    main()
