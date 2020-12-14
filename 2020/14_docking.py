#!/usr/bin/env python3

import sys
import re

from collections import namedtuple

MEMORY_SIZE = 1<<36

def masked_ints(mask):
    lsb = mask & -mask
    if lsb==0:
        yield 0
    else:
        for v in masked_ints(mask&~lsb):
            yield v
            yield v|lsb

class Mask:
    def __init__(self, string):
        self.xmask = int(string.replace('1','0').replace('X','1'), 2)
        self.ormask = int(string.replace('X','0'), 2)
        self.andmask = int(string.replace('X','1'), 2)

    def __call__(self, value):
        return ((value | self.ormask) & self.andmask)

    def addresses(self, address):
        address |= self.ormask
        address &= ~self.xmask
        for ad in masked_ints(self.xmask):
            yield address|ad

MemSet = namedtuple('MemSet', 'address value')

MASK_PTN = re.compile(r'mask = ([01X]+)$'.replace(' ', r'\s*'))
MEMSET_PTN = re.compile(r'mem\[#\] = #$'
            .replace('#', '([0-9]+)').replace(' ', r'\s*'))

def parse_instruction(string, maskptn=MASK_PTN, memptn=MEMSET_PTN):
    string = string.strip()
    m = re.match(memptn, string)
    if m:
       return MemSet(int(m.group(1)), int(m.group(2)))
    m = re.match(maskptn, string)
    if m:
        return Mask(m.group(1))
    raise ValueError(repr(string))

def run_instructions(memory, instructions):
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        else:
            memory[instruction.address] = mask(instruction.value)

def run_address_mask_instructions(memory, instructions):
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        else:
            for ad in mask.addresses(instruction.address):
                memory[ad] = instruction.value

def main():
    instructions = tuple(map(parse_instruction, sys.stdin))
    memory = {}
    run_instructions(memory, instructions)
    print("Sum of memory (value masking):", sum(memory.values()))

    memory = {}
    run_address_mask_instructions(memory, instructions)
    print("Sum of memory (address masking):", sum(memory.values()))

if __name__ == '__main__':
    main()
