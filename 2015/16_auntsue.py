#!/usr/bin/env python3

import sys
import operator
import functools

from collections import namedtuple

REQUIREMENTS = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

def parse_properties(reqs):
    for req in reqs:
        k,v = req.split(':')
        yield k.strip(), int(v.strip())

REQUIREMENTS = list(parse_properties(REQUIREMENTS.split('\n')))

class Sue:
    def __init__(self, number, props):
        self.number = number
        self.props = props
    @classmethod
    def parse(cls, line):
        name, props = line.split(':',1)
        assert name.startswith('Sue ')
        number = int(name[4:].strip())
        props = dict(parse_properties(props.split(',')))
        return cls(number, props)
    def __str__(self):
        return 'Sue %s'%self.number
    def matches(self, predicates):
        return all(predicate(self) for predicate in predicates)

AuntPredicate = namedtuple('AuntPredicate', 'key value operator')

AuntPredicate.__call__ = lambda self, aunt: (
    self.key not in aunt.props
    or self.operator(aunt.props[self.key], self.value)
)

def create_predicates(req, operators=None):
    predicates = []
    if operators is None:
        operators = {}
    for k,v in req:
        op = operators.get(k, operator.eq)
        predicates.append(AuntPredicate(k,v,op))
    return predicates

def main():
    lines = sys.stdin.read().strip().split('\n')
    sues = [Sue.parse(line) for line in lines]
    predicates = create_predicates(REQUIREMENTS)
    matching_sues = [sue for sue in sues if sue.matches(predicates)]
    print("Part 1. Matching sues:")
    for sue in matching_sues:
        print('',sue)
    operators = {
        'cats': operator.gt, 'trees': operator.gt,
        'pomeranians': operator.lt, 'goldfish': operator.lt,
    }
    predicates = create_predicates(REQUIREMENTS, operators)
    matching_sues = [sue for sue in sues if sue.matches(predicates)]
    print("Part 2. Matching sues:")
    for sue in matching_sues:
        print('',sue)

if __name__ == '__main__':
    main()
