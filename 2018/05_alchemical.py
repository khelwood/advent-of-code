#!/usr/bin/env python3

import sys

def pairs(x,y):
    return (x!=y and x.upper()==y.upper())

def react(seq):
    i = 0
    end = len(seq)-1
    while i < end:
        if pairs(seq[i], seq[i+1]):
            del seq[i:i+2]
            end -= 2
            i -= 1
        else:
            i += 1

def without(seq, letter):
    rem = {letter.upper(), letter.lower()}
    return [ch for ch in seq if ch not in rem]

def main():
    sequence = list(sys.stdin.read().strip())
    react(sequence)
    print("Reduced length:", len(sequence))
    best_length = len(sequence)
    for letter in map(chr, range(ord('a'), ord('z')+1)):
        newseq = without(sequence, letter)
        react(newseq)
        if len(newseq) < best_length:
            best_length = len(newseq)
            best_letter = letter
    print("Best letter to remove:", best_letter)
    print("Best length:", best_length)

if __name__ == '__main__':
    main()
