#!/usr/bin/env python3

import sys
import re
import random

def iter_new_codes(code, src, tgt):
    i = code.find(src)
    sl = len(src)
    while i>=0:
        yield code[:i]+tgt+code[i+sl:]
        i = code.find(src, i+1)

def replace_count(string, old, new):
    i = string.find(old)
    count = 0
    old_l = len(old)
    while i>=0:
        string = string[:i] + new + string[i+old_l:]
        count += 1
        i = string.find(old, i)
    return count, string

def replacement_outcomes(code, replacements, times=1):
    codes = [code]
    for i in range(times):
        seen = set()
        new_codes = []
        for code in codes:
            for src, tgt in replacements:
                for new_code in iter_new_codes(code, src, tgt):
                    if new_code not in seen:
                        seen.add(new_code)
                        new_codes.append(new_code)
        codes = new_codes
    return seen

def collapse(molecule, target, replacements):
    moves = 0
    lt = len(target)
    while len(molecule) > lt:
        k = next(((l,s) for s,l in replacements if l in molecule), None)
        if k is None:
            return None
        count, molecule = replace_count(molecule, *k)
        moves += count
    if molecule==target:
        return moves
    
def main():
    lines = sys.stdin.read().split('\n')
    code = lines[-1].strip()
    lines = filter(bool, map(str.strip, lines[:-1]))
    replacements = [tuple(map(str.strip, line.split('=>'))) for line in lines]
    outcomes = replacement_outcomes(code, replacements)
    print("Number of outcomes:", len(outcomes))
    least = len(replacements)*len(code)
    moves = None
    while moves is None:
        # I hate this solution, but it works.
        # Even iterating through permutations of the replacements
        #  didn't work (took too long)
        random.shuffle(replacements)
        moves = collapse(code, 'e', replacements)
    print("Moves:", moves)
if __name__ == '__main__':
    main()
