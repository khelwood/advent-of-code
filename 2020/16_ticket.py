#!/usr/bin/env python3

import sys

from collections import namedtuple

Rule = namedtuple('Rule', 'name ranges')
Range = namedtuple('Range', 'min max')
Rule.__contains__ = lambda self, value: any(value in r for r in self.ranges)
Range.__contains__ = lambda self, value: self.min <= value <= self.max

def parse_ranges(string):
    for part in string.split(' or '):
        a,_,b = part.partition('-')
        yield Range(int(a), int(b))

def parse_ticket(string):
    return tuple(map(int, string.strip().replace(',',' ').split()))

def parse_input():
    rules = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        name, _, rangestring = line.partition(':')
        name = name.strip()
        rules.append(Rule(name, tuple(parse_ranges(rangestring.strip()))))
    assert next(sys.stdin).strip()=='your ticket:'
    my_ticket = parse_ticket(next(sys.stdin))
    assert not next(sys.stdin).strip()
    assert next(sys.stdin).strip()=='nearby tickets:'
    nearby_tickets = tuple(map(parse_ticket, sys.stdin))
    return rules, my_ticket, nearby_tickets

def invalid_fields(rules, ticket):
    for value in ticket:
        if not any(value in rule for rule in rules):
            yield value

def narrow_rule_map(rule_map, solved_rules, solved_fields):
    for (rule, fields) in rule_map.items():
        if len(fields)==1 and rule not in solved_rules:
            field, = fields
            for r,f in rule_map.items():
                f.discard(field)
            rule_map[rule] = {field}
            solved_rules[rule] = field
            solved_fields[field] = rule
            return True
    field_map = {}
    for (rule, fields) in rule_map.items():
        for f in fields:
            if f not in field_map:
                field_map[f] = {rule}
            else:
                field_map[f].add(rule)
    for (field, rules) in field_map.items():
        if len(rules)==1 and field not in solved_fields:
            rule, = rules
            for r,f in rule_map.items():
                f.discard(field)
            rule_map[rule] = {field}
            solved_rules[rule] = field
            solved_fields[field] = rule
            return True
    return False

def identify_fields(rules, tickets):
    fields = tuple(map(tuple, zip(*tickets)))
    rule_map = {}
    for rule in rules:
        possible_fields = set()
        for i,field in enumerate(fields):
            if all(value in rule for value in field):
                possible_fields.add(i)
            rule_map[rule] = possible_fields
    solved_rules = {}
    solved_fields = {}
    while narrow_rule_map(rule_map, solved_rules, solved_fields):
        pass
    return solved_rules

def product(values):
    p = 1
    for v in values:
        p *= v
    return p

def main():
    rules, my_ticket, nearby = parse_input()
    error_rate = 0
    valid_tickets = [my_ticket]
    for ticket in nearby:
        valid = True
        for v in invalid_fields(rules, ticket):
            valid = False
            error_rate += v
        if valid:
            valid_tickets.append(ticket)
    print("Error rate:", error_rate)

    solved_rules = identify_fields(rules, valid_tickets)
    departure_rules = [rule for rule in rules
                        if rule.name.startswith('departure')]
    assert len(departure_rules)==6
    assert all(rule in solved_rules for rule in departure_rules)
    departure_product = product(my_ticket[solved_rules[rule]]
                        for rule in departure_rules)
    print("Departure product:", departure_product)

if __name__ == '__main__':
    main()
