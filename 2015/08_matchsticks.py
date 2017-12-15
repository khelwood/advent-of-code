#!/usr/bin/env python3

import sys
from ast import literal_eval

def main():
    lines = sys.stdin.read().strip().split('\n')
    content = [literal_eval(line) for line in lines]
    literal_length = sum(map(len, lines))
    content_length = sum(map(len, content))
    print("Literal length:", literal_length)
    print("Content length:", content_length)
    print("Difference:", literal_length-content_length)
    print()
    repr_lines = [ repr(line).replace('"','\\"') for line in lines]
    repr_length = sum(map(len, repr_lines))
    print("Repr length:", repr_length)
    print("Difference:", repr_length - literal_length)

if __name__ == '__main__':
    main()
