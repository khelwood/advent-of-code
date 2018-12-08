#!/usr/bin/env python3

import sys

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
        self._value = None
    def metadata_sum(self):
        return sum(self.metadata) + sum(map(Node.metadata_sum, self.children))
    def child_value(self, index):
        if 1 <= index <= len(self.children):
            return self.children[index-1].value()
        return 0
    def value(self):
        if self._value is None:
            self._value = self.calculate_value()
        return self._value
    def calculate_value(self):
        if self.children:
            return sum(self.child_value(i) for i in self.metadata)
        return sum(self.metadata)

def read_node(numbers):
    nc = next(numbers)
    nm = next(numbers)
    node = Node()
    for _ in range(nc):
        node.children.append(read_node(numbers))
    for _ in range(nm):
        node.metadata.append(next(numbers))
    return node

def main():
    root = read_node(int(x) for x in sys.stdin.read().split())
    print("Metadata sum:", root.metadata_sum())
    print("Value sum:", root.value())

if __name__ == '__main__':
    main()
