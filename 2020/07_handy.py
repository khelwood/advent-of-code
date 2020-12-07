#!/usr/bin/env python3

import sys
import re

from collections import namedtuple, Counter

Rule = namedtuple('Rule', 'subject contents')
NumberBag = namedtuple('NumberBag', 'number bag')

RULE_PATTERN = re.compile(r'([\w -]+) bags? contains? ([\d\w, -]+)\.$')
CONTENT_PATTERN = re.compile(r'(\d+) ([\w -]+) bags?$')

def parse_rule(line, pattern=RULE_PATTERN):
    m = re.match(pattern, line)
    if not m:
        raise ValueError(line)
    subject = m.group(1)
    contents = m.group(2)
    if contents=='no other bags':
        contents = ()
    else:
        contents = tuple(
            parse_content(part.strip()) for part in contents.split(',')
        )
    return Rule(subject, contents)

def parse_content(string, pattern=CONTENT_PATTERN):
    m = re.match(pattern, string)
    if not m:
        raise ValueError(string)
    n = int(m.group(1))
    bag = m.group(2)
    return NumberBag(n, bag)

def find_all_containers(rules, target):
    all_containers = set()
    new = {target}
    while new:
        old = new
        new = set()
        for rule in rules:
            if rule.subject in all_containers:
                continue
            if any(c.bag in old for c in rule.contents):
                new.add(rule.subject)
                all_containers.add(rule.subject)
    return all_containers

def count_contents(rules, target):
    bag_count = 0
    new = Counter({target:1})
    while new:
        old = new
        new = Counter()
        for rule in rules:
            subject_count = old[rule.subject]
            if subject_count > 0:
                for c in rule.contents:
                    new_count = subject_count*c.number
                    bag_count += new_count
                    new[c.bag] += new_count
    return bag_count

def main():
    rules = list(map(parse_rule, sys.stdin.read().strip().splitlines()))
    target = 'shiny gold'
    c = find_all_containers(rules, target)
    print(f"Bags that contain {target}: {len(c)}")
    d = count_contents(rules, target)
    print(f"Bags inside {target}: {d}")

if __name__ == '__main__':
    main()
