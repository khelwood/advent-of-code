#!/usr/bin/env python3

import sys
from itertools import permutations
from program import Program, parse_program_input

def find_highest_output(prog_input):
    highest = 0
    for phases in permutations(range(5), 5):
        last_out = 0
        for phase in phases:
            prog = Program(prog_input, [phase, last_out])
            prog.execute()
            last_out = prog.output_values[0]
        highest = max(highest, last_out)
    return highest

def run_feedback(prog_input):
    highest = 0
    for phases in permutations(range(5,10), 5):
        progs = [Program(prog_input, [phase]) for phase in phases]
        last_output = 0
        while progs[-1].pos >= 0:
            for prog in progs:
                prog.input_values.append(last_output)
                prog.execute_till_output()
                last_output = prog.output_values[-1]
        highest = max(highest, last_output)
    return highest

def main():
    prog_input = parse_program_input(sys.stdin.read())
    op1 = find_highest_output(prog_input)
    print("Highest output (simple):", op1)
    op2 = run_feedback(prog_input)
    print("Highest output (feedback):", op2)

if __name__ == '__main__':
    main()
