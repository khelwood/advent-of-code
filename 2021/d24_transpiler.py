#!/usr/bin/env python3

import sys

"""
Assumptions based on my task input:
* The ALU code includes four variables: w,x,y,z
* Input is always read into w.
* The first line of the ALU code is "inp w".
* There are fourteen input lines.

Compile the ALU code into fourteen functions, with parameters w,x,y,z
where w is the next item of data, and x,y,z are part of the state of the ALU.
Each function returns x,y,z.
For each function, cache it's results.

More advanced:
Cache the result of validating the first N parts of the data, and reuse it
for the subsequent parts.
"""


def compile_line(line):
    cmd, *args = line.split()
    if len(args)==2:
        a,b = args
    else:
        a, = args
    # 'inp' is not compiled to a statement
    if cmd=='add':
        if b!='0':
            yield f'{a} += {b}'
        return
    if cmd=='mul':
        if b=='0':
            yield f'{a} = 0'
        elif b!='1':
            yield f'{a} *= {b}'
        return
    if cmd=='div':
        if b!='1':
            yield f'if ({a} < 0) != ({b} < 0):'
            yield f'    {a} = -(abs({a}) // abs({b}))'
            yield 'else:'
            yield f'    {a} //= {b}'
        return
    if cmd=='mod':
        yield f'{a} %= {b}'
        return
    if cmd=='eql':
        yield f'{a} = int({a}=={b})'
        return
    raise ValueError("Invalid line: "+repr(line))

def iter_candidates():
    num = 10**14
    while True:
        num -= 1
        data = tuple(int(d) for d in str(num))
        if 0 not in data:
            yield data

def alu_to_python_def(lines):
    code = []
    for line in lines:
        for statement in compile_line(line):
            code.append(statement)
    code.append('return x,y,z')
    code = ['    '+line for line in code]
    code.insert(0, 'def func(w,x,y,z):')
    return '\n'.join(code)

def compile_alu(lines, cache=False):
    code = alu_to_python_def(lines)
    space = {}
    exec(code, space)
    if not cache:
        return space['func']
    return cached_function(space['func'])

def cached_function(func):
    def cached_func(*args, _cache={}, _wrapped_func=func):
        if args in _cache:
            return _cache[args]
        r = _wrapped_func(*args)
        _cache[args] = r
        return r
    cached_func.__name__ = func.__name__
    return cached_func

def chain_functions(funcs):
    digits = range(9,0,-1)
    def find_w(x,y,z, func=funcs[-1]):
        for w in digits:
            a,b,c = func(w,x,y,z)
            if c==0:
                return (w,)
        return None
    last_func = cache(find_w)
    for func in funcs[-2:-1:-1]:
        def find_w(x,y,z, func=func, next_func=last_func):
            for w in digits:
                a,b,c = func(w,x,y,z)
                sol = next_func(a,b,c)
                if seq:
                    return (w,) + sol
            return None
        last_func = cache(find_w)
    return last_func


def create_functions(lines, cache=False):
    funcs = []
    last_inp = -1
    for index,line in enumerate(lines):
        if line.startswith('inp'):
            if last_inp >= 0:
                funcs.append(compile_alu(lines[last_inp+1:index], cache=cache))
            last_inp = index
    funcs.append(compile_alu(lines[last_inp+1:]))
    return tuple(funcs)


def main():
    lines = sys.stdin.read().strip().splitlines()
    funcs = create_functions(lines, cache=True)
    solver = chain_functions(funcs)
    result = solver(0,0,0)
    print("Result:", result)

if __name__ == '__main__':
    main()
