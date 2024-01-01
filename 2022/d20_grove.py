#!/usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass
class Node:
    value: int
    prev = None
    next = None

    def shift(self, d, num_nodes):
        d %= (num_nodes-1)
        if d==0:
            return
        self.prev.next = self.next
        self.next.prev = self.prev
        cur = self
        if 2*d < num_nodes:
            for _ in range(d):
                cur = cur.next
            # place after cur
            self.next = cur.next
            cur.next.prev = self
            self.prev = cur
            cur.next = self
        else:
            for _ in range(num_nodes-1-d):
                cur = cur.prev
            # place before cur
            self.prev = cur.prev
            cur.prev.next = self
            self.next = cur
            cur.prev = self

    def __iter__(self):
        yield self
        cur = self.next
        while cur is not self:
            yield cur
            cur = cur.next

    def find_relative(self, d, num_nodes):
        d %= num_nodes
        if d==0:
            return self
        cur = self
        if 2*d < num_nodes:
            for _ in range(d):
                cur = cur.next
        else:
            for _ in range(num_nodes-d):
                cur = cur.prev
        return cur


def create_nodes(values):
    num_nodes = len(values)
    nodes = list(map(Node, values))
    for i,node in enumerate(nodes):
        node.prev = nodes[i-1]
        node.next = nodes[(i+1)%num_nodes]
    return nodes

def grove(node, num_nodes):
    total = 0
    for _ in range(3):
        node = node.find_relative(1000, num_nodes)
        total += node.value
    return total

def main():
    values = list(map(int, sys.stdin.read().split()))
    zero_index = values.index(0)
    nodes = create_nodes(values)
    num_nodes = len(nodes)
    for node in nodes:
        node.shift(node.value, num_nodes)
    print("Part 1:", grove(nodes[zero_index], num_nodes))

    nodes = create_nodes([n*811589153 for n in values])
    for _ in range(10):
        for node in nodes:
            node.shift(node.value, num_nodes)
    print("Part 2:", grove(nodes[zero_index], num_nodes))

if __name__ == '__main__':
    main()
