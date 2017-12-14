#!/usr/bin/env python3

import sys
import re

def evaluate_once(func):
    def evaluate_and_replace(self):
        value = func(self)
        self.__dict__[func.__name__] = value
        return value
    evaluate_and_replace.__name__ = func.__name__
    return property(evaluate_and_replace)

class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []

    @evaluate_once
    def total_weight(self):
        return self.weight + sum(x.total_weight for x in self.children)

    @evaluate_once
    def balanced(self):
        return all_eq(x.total_weight for x in self.children)

    def find_problem(self):
        if self.balanced:
            return self
        if not all(x.balanced for x in self.children):
            n = next(x for x in self.children if not x.balanced)
            return n.find_problem()
        w = self.children[0].total_weight
        if w != self.children[1].total_weight:
            w = self.children[2].total_weight
        return next(x for x in self.children if x.total_weight!=w)

    def find_correct_weight(self):
        p = self.parents[0]
        sibling = p.children[p.children[0]==self]
        return sibling.total_weight - self.total_weight + self.weight

def all_eq(seq, sentinel=object()):
    it = iter(seq)
    n = next(it, sentinel)
    return n is sentinel or all(x==n for x in it)

class NodeDict(dict):
    def __missing__(self, key):
        value = self[key] = Node(key)
        return value

NODE_PTN = re.compile(r'^(\w+) \(([0-9]+)\)(?: -> ([\w, ]+))?$')

def process(line, nodes):
    m = NODE_PTN.match(line)
    name, weight, c = [(m.group(i) or '').strip() for i in range(1,4)]
    node = nodes[name]
    if c:
        children = [nodes[name] for name in c.replace(',',' ').split()]
        for c in children:
            c.parents.append(node)
    else:
        children = []
    node.weight = int(weight)
    node.children = children

def create_nodes(lines):
    nodes = NodeDict()
    for line in lines:
        process(line, nodes)
    return nodes

def find_root(nodes):
    return next(n for n in nodes.values() if not n.parents)

def main():
    lines = sys.stdin.read().strip().split('\n')
    nodes = create_nodes(lines)
    print("%s nodes"%len(nodes))
    root = find_root(nodes)
    print("Root:", root.name)
    problem = root.find_problem()
    print("Problem: %s (%s)"%(problem.name, problem.weight))
    correct = problem.find_correct_weight()
    print("Correct weight:", correct)

if __name__=='__main__':
    main()
