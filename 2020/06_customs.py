#!/usr/bin/env python3

import sys

def input_blocks(data):
    return data.split('\n\n')

def block_intersection(block):
    lines = block.splitlines()
    return set.intersection(*map(set, lines))

def main():
    blocks = input_blocks(sys.stdin.read().strip())
    any_sum = sum(len(set(filter(str.isalpha, block))) for block in blocks)
    print("Any sum:", any_sum)
    all_sum = sum(len(block_intersection(block)) for block in blocks)
    print("All sum:", all_sum)

if __name__ == '__main__':
    main()
