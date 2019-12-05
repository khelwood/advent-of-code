#!/usr/bin/env python3

import sys
import operator

POS_MODE = 0
VALUE_MODE = 1

ADD_OP = 1
MUL_OP = 2
INPUT_OP = 3
OUTPUT_OP = 4
JIT_OP = 5
JIF_OP = 6
LT_OP = 7
EQ_OP = 8
END_OP = 99

class Program:
    def __init__(self, data):
        self.data = list(data)
        self.pos = 0
        self.output = []
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data[index] = value
    def __iadd__(self, delta):
        self.pos += delta
    def load_input(self, values):
        self.input = iter(values)
    def emit(self, value):
        self.output.append(value)
    def next_input(self):
        return next(self.input)
    def get_value(self, index):
        mixed_op = self[self.pos]
        value = self[self.pos + index]
        if index==1:
            d = 100
        elif index==2:
            d = 1000
        else:
            raise ValueError("Cannot get value for index %s"%index)
        if (mixed_op//d)%10==VALUE_MODE:
            return value
        return self[value]
    def get_pos(self, index):
        return self[self.pos + index]
    def binop(self, func):
        x = self.get_value(1)
        y = self.get_value(2)
        z = self.get_pos(3)
        self[z] = func(x,y)
        self += 4
    def jumpif(self, guard):
        x = self.get_value(1)
        if bool(guard)==bool(x):
            self.pos = self.get_value(2)
        else:
            self += 3
    def cmpop(self, func):
        x = self.get_value(1)
        y = self.get_value(2)
        z = self.get_pos(3)
        self[z] = int(func(x, y))
        self += 4
    def input(self):
        p = self.get_pos(1)
        self[p] = self.next_input()
        self += 2
    def output(self):
        v = self.get_value(1)
        self.emit(v)
        self += 2
    def end(self):
        self.pos = -1
    def perform_command(self):
        OP_FUNC[self[self.pos]%100](self)
    def execute(self):
        while self.pos >= 0:
            self.perform_command()

OP_FUNC = {
    ADD_OP: (lambda prog: prog.binop(operator.add)),
    MUL_OP: (lambda prog: prog.binop(operator.mul)),
    INPUT_OP: Program.input,
    OUTPUT_OP: Program.output,
    END_OP: Program.end,
    JIT_OP: (lambda prog: prog.jumpif(True)),
    JIF_OP: (lambda prog: prog.jumpif(False)),
    LT_OP: (lambda prog: prog.cmpop(operator.lt)),
    EQ_OP: (lambda prog: prog.cmpop(operator.eq)),
}

def input_data():
    return list(map(int, sys.stdin.read().replace(',',' ').split()))

def main():
    data = input_data()
    prog = Program(data)
    prog.load_input([1])
    prog.execute()
    print("First program output:", prog.output[-1])
    prog = Program(data)
    prog.load_input([5])
    prog.execute()
    print("Second program output:", prog.output[-1])

if __name__ == '__main__':
    main()
