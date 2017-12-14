#!/usr/bin/env python3

import sys
from assembunny import make_program, OutputError, OutputSuccess

def main():
    lines = sys.stdin.read().strip().split('\n')
    for i in range(0,1000):
        print(" (Trying %s)"%i, end='\r')
        prog = make_program(lines, True, True)
        prog['a'] = i
        try:
            prog.run()
        except OutputError:
            continue
        except OutputSuccess:
            print("\nSuccess!")
            print("Result:",i)
            return

if __name__ == '__main__':
    main()
