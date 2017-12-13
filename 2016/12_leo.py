#!/usr/bin/env python3

import sys

from assembunny import make_program

def main():
    lines = sys.stdin.read().strip().split('\n')
    prog = make_program(lines)
    print("Running...")
    prog.run()
    result = prog['a']
    print("Part 1:", result)
    # PART 2:
    prog = make_program(lines)
    prog['c'] = 1
    print("Running...")
    prog.run()
    result = prog['a']
    print("Part 2:", result)
            
if __name__ == '__main__':
    main()
