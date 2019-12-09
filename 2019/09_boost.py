#!/usr/bin/env python3

import sys
from program import Program, parse_program_input

def main():
    data = parse_program_input(sys.stdin.read())
    prog = Program(data, [1])
    prog.execute()
    print(prog.output_values)
    prog = Program(data, [2])
    prog.execute()
    print(prog.output_values)

if __name__ == '__main__':
    main()
