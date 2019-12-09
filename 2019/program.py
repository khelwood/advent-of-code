import operator

POS_MODE = 0
VALUE_MODE = 1
RELATIVE_MODE = 2

ADD_OP = 1
MUL_OP = 2
INPUT_OP = 3
OUTPUT_OP = 4
JIT_OP = 5
JIF_OP = 6
LT_OP = 7
EQ_OP = 8
RBO_OP = 9
END_OP = 99

class Program:
    def __init__(self, data, input_values=None):
        self.data = list(data)
        self.pos = 0
        self.output_values = []
        self.input_values = input_values
        self.halted = False
        self.relative_base = 0
        self.extra_data = {}
    def __getitem__(self, index):
        if index < len(self.data):
            return self.data[index]
        return self.extra_data.get(index, 0)
    def __setitem__(self, index, value):
        if index < len(self.data):
            self.data[index] = value
        else:
            self.extra_data[index] = value
    def load_input(self, values):
        self.input_values = input_values
    def emit(self, value):
        self.output_values.append(value)
    def next_input(self):
        if not self.input_values:
            raise ProgramInputError()
        return self.input_values.pop(0)
    def get_value(self, index):
        return self[self.get_pos(index)]
    def get_pos(self, index):
        mixed_op = self[self.pos]
        if index==1:
            d = 100
        elif index==2:
            d = 1000
        elif index==3:
            d = 10_000
        else:
            raise ValueError("Cannot get pos for index %s"%index)
        mode = (mixed_op//d)%10
        if mode==POS_MODE:
            return self[self.pos + index]
        if mode==VALUE_MODE:
            return self.pos + index
        return self[self.pos + index] + self.relative_base
    def binop(self, func):
        x = self.get_value(1)
        y = self.get_value(2)
        z = self.get_pos(3)
        self[z] = func(x,y)
        self.pos += 4
    def jumpif(self, guard):
        x = self.get_value(1)
        if bool(guard)==bool(x):
            self.pos = self.get_value(2)
        else:
            self.pos += 3
    def cmpop(self, func):
        x = self.get_value(1)
        y = self.get_value(2)
        z = self.get_pos(3)
        self[z] = int(func(x, y))
        self.pos += 4
    def input(self):
        p = self.get_pos(1)
        self[p] = self.next_input()
        self.pos += 2
    def output(self):
        v = self.get_value(1)
        self.emit(v)
        self.pos += 2
    def end(self):
        self.pos = -1
    def rboffset(self):
        self.relative_base += self.get_value(1)
        self.pos += 2
    def perform_command(self):
        OP_FUNC[self[self.pos]%100](self)
    def execute(self):
        while self.pos >= 0:
            self.perform_command()
    def execute_till_output(self):
        op = len(self.output_values)
        while self.pos >= 0 and len(self.output_values)==op:
            self.perform_command()

class ProgramInputError(Exception):
    pass


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
    RBO_OP: Program.rboffset,
}

def parse_program_input(text):
    return list(map(int, text.replace(',',' ').split()))
