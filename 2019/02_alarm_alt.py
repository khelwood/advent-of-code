#!/usr/bin/env python3

import sys
import itertools

from program import parse_program_input, Program

def find_noun_verb(data, target):
    for noun,verb in itertools.product(range(100), repeat=2):
         prog = Program(data)
         prog[1] = noun
         prog[2] = verb
         prog.execute()
         if prog[0]==target:
             return (noun,verb)
    return None

def main():
    data = parse_program_input(sys.stdin.read())
    program = Program(data)
    program[1] = 12
    program[2] = 2
    program.execute()
    print("Part 1", program[0])

    target = 19690720
    noun, verb = find_noun_verb(data, target)
    print("Part 2", 100*noun + verb)

if __name__ == '__main__':
    main()
