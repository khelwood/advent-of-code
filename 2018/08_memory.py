#!/usr/bin/env python3

import sys

class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata
        self.value = self.calculate_value()
    def metadata_sum(self):
        return sum(self.metadata) + sum(map(Node.metadata_sum, self.children))
    def child_value(self, index):
        if 1 <= index <= len(self.children):
            return self.children[index-1].value
        return 0
    def calculate_value(self):
        if self.children:
            return sum(map(self.child_value, self.metadata))
        return sum(self.metadata)

def read_node(numbers):
    nc = next(numbers)
    nm = next(numbers)
    children = [read_node(numbers) for _ in range(nc)]
    metadata = [next(numbers) for _ in range(nm)]
    return Node(children, metadata)

def main():
    root = read_node(map(int, sys.stdin.read().split()))
    print("Metadata sum:", root.metadata_sum())
    print("Value sum:", root.value)

if __name__ == '__main__':
    main()
