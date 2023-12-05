#!/usr/bin/env python3

import sys

# w, z, thing1, thing2
def digit_trans(*args, cache={}):
    if args in cache:
        return cache[args]
    w, z, thing1, thing2 = args
    x = z%26 + thing1
    if x!=w:
        z *= 26
    y = w + thing2
    y *= x
    z += y
    return z

def varname(name, suffix):
    return (name+str(suffix)) if name in {'w','x','y','z'} else name

def compile_line(line, suffix):
    cmd, *args = line.split()
    args = [varname(x, suffix) for x in args]
    if len(args)==2:
        a,b = args
    else:
        a, = args
    # 'inp' works differently
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
        if b=='1':
            return
        if b.startswith('-'):
            yield f'if {a} < 0:'
            yield f'    {a} //= {b}'
            yield 'else:'
            yield f'    {a} = -({a} // {b[1:]})'
        elif b.isdigit():
            yield f'if {a} < 0:'
            yield f'    {a} = -((-{a}) // {b})'
            yield 'else:'
            yield f'    {a} //= {b}'
        else:
            yield f'if ({a} < 0) != ({b} < 0):'
            yield f'    {a} = -(abs({a})//abs({b}))'
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

def compile(lines):
    setup = ['ran = range(9,0,-1)',
        'x0=y0=z0=0',
        'checked = [set() for _ in range(14)]']
    ind = '    '
    code = ['def solve():'] + [ind + line for line in setup]
    suffix=-1
    for line in lines:
        if line.startswith('inp'):
            if suffix >= 0:
                code.append(ind + f'x{suffix} %= 26')
                code.append(ind + f'if (x{suffix},y{suffix},z{suffix}) in checked[{suffix}]:')
                code.append(ind + '    continue')
                code.append(ind + f'checked[{suffix}].add((x{suffix}, y{suffix}, z{suffix}))')
            suffix += 1
            code.append(ind + f'for w{suffix} in ran:')
            ind += '   '
            if suffix > 0:
                for v in 'xyz':
                    code.append(ind + f'{v}{suffix} = {v}{suffix-1}')
        else:
            for statement in compile_line(line, suffix):
                code.append(ind + statement)
    code.append(ind+f'if z{suffix}==0:')
    code.append(ind+'    return (w0,w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w13)')
    d = {}
    print('\n'.join(code))
    exec('\n'.join(code), d)
    return d['solve']


def main():
    solve = compile(sys.stdin.read().strip().splitlines())
    print(solve())



if __name__ == '__main__':
    main()
