#!/usr/bin/env python3

import sys

def count_no_repeats(items):
    return sum(len(item)==len(set(item)) for item in items)

def main():
    lines = sys.stdin.read().strip().split('\n')
    word_lines = [line.split() for line in lines]
    num_valid = count_no_repeats(word_lines)
    print("Num valid (no repeated words):", num_valid)
    num_valid = count_no_repeats(
        [''.join(sorted(word)) for word in line] for line in word_lines
    )
    print("Num valid (no anagrams):", num_valid)
    
if __name__ == '__main__':
    main()
