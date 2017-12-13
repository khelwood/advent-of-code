#!/usr/bin/env python3

import sys

from assembunny import make_program

def main():
    if len(sys.argv) <= 1:
        exit("Usage: %s <number>"%sys.argv[0])
    start = int(sys.argv[1])
    lines = sys.stdin.read().strip().split('\n')
    prog = make_program(lines, toggles=True)
    prog.verbose = True
    prog['a'] = start
    print("Running...")
    prog.run()
    result = prog['a']
    print("Result:", result)
    
if __name__ == '__main__':
    main()
