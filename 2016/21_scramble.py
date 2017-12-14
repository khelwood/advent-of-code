#!/usr/bin/env python3

import sys
import re
import itertools

START_CODE = 'abcdefgh'
END_CODE = 'fbgdceah'

def swap_position(code, x, y):
    code[x], code[y] = code[y], code[x]

def swap_letter(code, x, y):
    i = code.index(x)
    j = code.index(y)
    code[i], code[j] = y, x

def rotate_left(code, steps):
    rotate_right(code, -steps)
    
def rotate_right(code, steps):
    steps %= len(code)
    if steps:
        code[:] = code[-steps:] + code[:-steps]

def rotate_arcane(code, letter):
    i = code.index(letter)
    rotate_right(code, 1 + i + (i>=4))

def unrotate_arcane(code, letter):
    i = code.index(letter)
    if i%2:
        rotate_right(code, i//-2) # 5//-2==-3 etc.
    elif i:
        rotate_right(code, 3-i//2)
    else:
        rotate_right(code, 7)

def reverse_positions(code, x, y):
    code[x:y+1] = code[y::-1] if x==0 else code[y:x-1:-1]

def move_position(code, x, y):
    code.insert(y, code.pop(x))

def unmove_position(code, x, y):
    move_position(code, y, x)

CODE_FINDER = re.compile('#|X|R')

class CodeOperation:
    def __init__(self, regex, fn, unfn=None):
        self.desc = regex
        self.ptn = re.compile('^'+regex.replace('#','(-?[0-9]+)')
                                  .replace('X','(\w)')+'$')
        self.params = CODE_FINDER.findall(regex)
        self._fn = fn
        self._unfn = unfn or fn
    def __call__(self, command, code, backwards=False):
        m = self.ptn.match(command)
        if not m:
            return False
        args = [int(m.group(i)) if p=='#' else m.group(i)
                    for i,p in enumerate(self.params, 1)]
        [self._fn, self._unfn][backwards](code, *args)
        return True

code_ops = (
    CodeOperation('swap position # with position #', swap_position),
    CodeOperation('swap letter X with letter X', swap_letter),
    CodeOperation('rotate right # steps?', rotate_right, rotate_left),
    CodeOperation('rotate left # steps?', rotate_left, rotate_right),
    CodeOperation('rotate based on position of letter X',
                      rotate_arcane, unrotate_arcane),
    CodeOperation('reverse positions # through #', reverse_positions),
    CodeOperation('move position # to position #',
                      move_position, unmove_position),
)

def param_values(params):
    letters = START_CODE
    span = range(8) if params[0]=='#' else letters
    if len(params)==1:
        return map(lambda i: (i,), span)
    if span==letters:
        return itertools.product(letters, letters)
    return itertools.combinations(span, 2)
    
def test_code_ops():
    letters = START_CODE
    for code_op in code_ops:
        for args in param_values(code_op.params):
            code = list(letters)
            code_op._fn(code, *args)
            coded = code[:]
            code_op._unfn(code, *args)
            if code!=list(letters):
                print("FAIL: reverse %r with %r on %r produced %r instead of %r."%
                      (code_op.desc, args, ''.join(coded), ''.join(code), letters))

def main(start, end):
    commands = sys.stdin.read().split('\n')
    code = list(start)
    for command in commands:
        if not any(code_op(command, code) for code_op in code_ops):
            raise ValueError(repr(command))
    print("Part 1.", ''.join(code))
    # Part 2
    code = list(end)
    for command in reversed(commands):
        if not any(code_op(command, code, True) for code_op in code_ops):
            raise ValueError(repr(command))
    print("Part 2.", ''.join(code))

if __name__ == '__main__':
    # test_code_ops()
    start = sys.argv[1] if len(sys.argv) > 1 else START_CODE
    end = sys.argv[2] if len(sys.argv) > 2 else END_CODE
    main(start, end)
