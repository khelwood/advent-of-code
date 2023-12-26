#!/usr/bin/env python3

import sys
import networkx as nx

def read_graph(lines):
    graph = nx.Graph()
    for line in lines:
        c = line.index(':')
        left = line[:c].strip()
        rights = line[c+1:].strip().split()
        for right in rights:
            graph.add_edge(left, right)
    return graph

def main():
    lines = sys.stdin.read().strip().splitlines()
    graph = read_graph(lines)
    cut = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(cut)
    n = 1
    for sub in nx.connected_components(graph):
        n *= len(sub)
    print(n)

if __name__ == '__main__':
    main()
