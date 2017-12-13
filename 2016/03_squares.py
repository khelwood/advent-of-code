#!/usr/bin/env python3

import sys

def valid_triangle(lengths):
    return 2*max(lengths) < sum(lengths)

def main():
    lines = sys.stdin.read().strip().split('\n')
    data = [[int(n) for n in line.split()] for line in lines]
    print("Valid row triangles:", sum(map(valid_triangle, data)))
    cols = list(zip(*data))
    col_data = [col[i:i+3] for col in cols for i in range(0, len(col), 3)]
    print("Valid column triangles:", sum(map(valid_triangle, col_data)))

if __name__ == '__main__':
    main()
