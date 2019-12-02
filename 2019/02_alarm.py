#!/usr/bin/env python3

import sys

ADD_OP = 1
MUL_OP = 2
END_OP = 99

def run(data):
    for i in range(0, len(data), 4):
        op = data[i]
        if op==END_OP:
            return
        a = data[i+1]
        b = data[i+2]
        r = data[i+3]
        if op==ADD_OP:
            data[r] = data[a] + data[b]
        elif op==MUL_OP:
            data[r] = data[a] * data[b]
        else:
            raise ValueError("Invalid opcode: %s"%op)

def find_noun_verb(og, target):
    for noun in range(0,100):
        for verb in range(0,100):
            data = og[:]
            data[1] = noun
            data[2] = verb
            run(data)
            if data[0]==target:
                return (noun, verb)

def main():
    og = list(map(int, sys.stdin.read().replace(',',' ').split()))
    data = og[:]
    data[1] = 12
    data[2] = 2
    run(data)
    print("Part 1", data[0])

    target = 19690720
    noun, verb = find_noun_verb(og, target)
    print("Part 2", 100*noun + verb)

if __name__ == '__main__':
    main()
