#!/usr/bin/env python3

import re
import pyperclip

class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self._total_weight = None
        self._balanced = None
    @property
    def total_weight(self):
        if self._total_weight is None:
            self._total_weight = self.weight + sum(x.total_weight for x in self.children)
        return self._total_weight
    def __repr__(self):
        return f'Node("{self.name}")'
    @property
    def balanced(self):
        if self._balanced is None:
            self._balanced = all_eq(x.total_weight for x in self.children)
        return self._balanced
        
    def find_problem(self):
        if self.balanced:
            return self
        if not all(x.balanced for x in self.children):
            n = next(x for x in self.children if not x.balanced)
            return n.find_problem()
        
        w=self.children[0].total_weight
        if w!=self.children[1].total_weight:
            w = self.children[2].total_weight
        return next(x for x in self.children if x.total_weight!=w)
    def find_correct_weight(self):
        p = self.parents[0]
        sibling = p.children[p.children[0]==self]
        return sibling.total_weight - self.total_weight + self.weight

def all_eq(seq):
    it = iter(seq)
    n = next(it, None)
    if n is None:
        return True
    return all(x==n for x in it)

class NodeDict(dict):
    def __missing__(self, key):
        value = self[key] = Node(key)
        return value

def process(line, nodes, ptn=re.compile(r'^(\w+)%\(([0-9]+)\)%(->%[\w, ]+)?$'
                                     .replace('%', r'\s*'))):
    m = ptn.match(line)
    name, weight, c = [(m.group(i) or '').strip() for i in range(1,4)]
    node = nodes[name]
    if c:
        children = [nodes[name] for name in c[2:].replace(',',' ').split()]
        for c in children:
            c.parents.append(node)
    else:
        children = []
    node.weight = int(weight)
    node.children = children

def create_nodes(lines):
    if isinstance(lines, str):
        lines = lines.split('\n')
    nodes = NodeDict()
    for line in lines:
        line = line.strip()
        if line:
            process(line, nodes)
    return nodes

def find_root(nodes):
    return next(n for n in nodes.values() if not n.parents)

def main():
    print("Copy nodes to clipboard and press enter.")
    input(">")
    block = pyperclip.paste()
    nodes = create_nodes(block)
    print("%s nodes"%len(nodes))
    root = find_root(nodes)
    print("Root: %s"%root)
    problem = root.find_problem()
    print("Problem: %s (%s)"%(problem, problem.weight))
    correct = problem.find_correct_weight()
    print("Correct weight: %s"%correct)

if __name__=='__main__':
    main()
