#!/usr/bin/env python3

import sys

def recipe_sequence():
    """Yields the growing list of numbers in the recipe sequence."""
    recipes = [3,7]
    elf1 = 0
    elf2 = 1
    while True:
        r1 = recipes[elf1]
        r2 = recipes[elf2]
        total = r1 + r2
        if total < 10:
            recipes.append(total)
        else:
            recipes.extend(divmod(total, 10))
        yield recipes
        lr = len(recipes)
        elf1 = (elf1 + 1 + r1) % lr
        elf2 = (elf2 + 1 + r2) % lr

def solve_1(num_rec):
    end = num_rec + 10
    for rec in recipe_sequence():
        if len(rec) >= end:
            break
    return ''.join(map(str, rec[num_rec:end]))

def solve_2(sequence):
    """Checking the recipe using a slice turns out to be
    faster than using all(...) and checking each character.
    An optimisation might be to hard-code checking of the
    first character (or the first few characters) of the sequence,
    so the list slicing is avoided in nearly all cases."""
    ls = len(sequence)
    for rec in recipe_sequence():
        if rec[-ls:] == sequence:
            return len(rec) - ls
        if rec[-ls-1:-1] == sequence:
            return len(rec) - 1 - ls

def main():
    code = sys.argv[1]
    print("Part 1:", solve_1(int(code)))
    print("Part 2:", solve_2([int(ch) for ch in code]))

if __name__ == '__main__':
    main()
