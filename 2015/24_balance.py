#!/usr/bin/env python3

import sys
import operator
import functools
import itertools

def product(sequence):
    return functools.reduce(operator.mul, sequence, 1)

def iter_groups(weights, target):
    if not isinstance(weights, list):
        weights = list(weights)
    for i,weight in enumerate(weights):
        if weight > target:
            continue
        ws = {weight}
        if weight==target:
            yield ws
        for rest in iter_groups(weights[i+1:], target-weight):
            yield (ws | rest)

def valid_third(weights, gp, target):
    for g in iter_groups(set(weights)-set(gp), target):
        return True
    return False

def valid_quarter(weights, gp, target):
    weights = set(weights)-set(gp)
    for alpha in iter_groups(weights, target):
        alpha_c = weights-alpha
        for beta in iter_groups(weights, target):
            return True
    return False
            
def best_group(weights, num):
    target = sum(weights)//num
    if target in weights:
        return (target,)
    group_size = 1
    best_gp = None
    best_qe = None
    valid = valid_third if num==3 else valid_quarter
    while best_gp is None:
        group_size += 1
        for gp in itertools.combinations(weights, group_size):
            if sum(gp)!=target:
                continue
            qe = product(gp)
            if best_gp is not None and qe >= best_qe:
                continue
            if valid(weights, gp, target):
                best_gp = gp
                best_qe = qe
    return best_gp

def main():
    weights = [int(n) for n in sys.stdin.read().split()]
    bg = best_group(weights, 3)
    print("Best group (from 3):", bg)
    print("QE:", product(bg))
    bg = best_group(weights, 4)
    print("Best group (from 4):", bg)
    print("QE:", product(bg))

if __name__ == '__main__':
    main()
