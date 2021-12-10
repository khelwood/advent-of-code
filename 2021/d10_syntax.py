#!/usr/bin/env python3

import sys

BRACKETS = {'(':')', '[':']', '{':'}', '<':'>'}
COMPLETION_SCORES = {')':1, ']':2, '}':3, '>':4}

def find_error(line, brackets=BRACKETS):
    stack = []
    for ch in line:
        r = brackets.get(ch)
        if r is not None:
            stack.append(r)
            continue
        x = stack.pop()
        if x!=ch:
            return ch
    return stack

def score_completion(stack, cs=COMPLETION_SCORES):
    score = 0
    for ch in reversed(stack):
        score *= 5
        score += cs[ch]
    return score

def median(values):
    return sorted(values)[len(values)//2]

def main():
    lines = sys.stdin.read().strip().splitlines()
    scores = {')':3, ']':57, '}':1197, '>':25137}
    total_score = 0
    stacks = []
    for line in lines:
        result = find_error(line)
        if isinstance(result, list):
            stacks.append(result)
        else:
            total_score += scores[result]
    print("Error score:", total_score)
    comp_scores = list(map(score_completion, stacks))
    print("Completion score:", median(comp_scores))

if __name__ == '__main__':
    main()
