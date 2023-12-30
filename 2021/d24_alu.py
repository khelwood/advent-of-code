#!/usr/bin/env python3

import sys
import re
import z3

PATTERN_1 = re.compile(r'''
inp w
mul x 0
add x z
mod x 26
div z 1
add x -?\d+
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (-?\d+)
mul y x
add z y
'''.strip())

PATTERN_2 = re.compile(r'''
inp w
mul x 0
add x z
mod x 26
div z 26
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y -?\d+
mul y x
add z y
'''.strip())


def solve(text:str, least:bool):
    chunk = 0
    pushes = []
    wvars = {s:z3.Int(s) for s in (f'w{i}' for i in range(1,15))}
    sol = z3.Solver()
    while text:
        command = None
        m = PATTERN_1.match(text)
        if m:
            command = 'push'
        else:
            m = PATTERN_2.match(text)
            if m:
                command = 'pop'
        if not command:
            raise ValueError(repr(text))
        d = int(m.group(1))
        chunk += 1
        w = f"w{chunk}"
        wvar = wvars[w]
        sol.add(1 <= wvar)
        sol.add(wvar <= 9)

        if command=='push':
            pushes.append((w,d))
        else:
            v,e = pushes.pop()
            sol.add(wvar == wvars[v] + (e + d))
        text = text[m.end():].strip()
    while sol.check()==z3.sat:
        model = sol.model()
        ws = [model[wvars[f'w{i}']].as_long() for i in range(1,15)]
        answer = int(''.join(map(str, ws)))
        varsum = wvars['w14']
        tens = 1
        for i in range(13,0,-1):
            tens *= 10
            varsum += tens*wvars[f'w{i}']
        sol.add((varsum < answer) if least else (varsum > answer))
    return answer

def main():
    text = sys.stdin.read().strip()
    print(solve(text, False))
    print(solve(text, True))


if __name__ == '__main__':
    main()
