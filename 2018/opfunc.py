import operator
from enum import Enum

def first(a,b=None):
    return a

class OpFunc(Enum):
    ADDR = (operator.add, True, True)
    ADDI = (operator.add, True, False)
    MULR = (operator.mul, True, True)
    MULI = (operator.mul, True, False)
    BANR = (operator.and_, True, True)
    BANI = (operator.and_, True, False)
    BORR = (operator.or_, True, True)
    BORI = (operator.or_, True, False)
    SETR = (first, True, None)
    SETI = (first, False, None)
    GTIR = (operator.gt, False, True)
    GTRI = (operator.gt, True, False)
    GTRR = (operator.gt, True, True)
    EQIR = (operator.eq, False, True)
    EQRI = (operator.eq, True, False)
    EQRR = (operator.eq, True, True)
    @property
    def function(self):
        return self.value[0]
    @property
    def areg(self):
        return self.value[1]
    @property
    def breg(self):
        return self.value[2]
    def __repr__(self):
        return 'OpFunc.'+self.name
    def __call__(self, registers, a, b):
        if self.areg:
            a = registers[a]
        if self.breg:
            b = registers[b]
        return self.function(a,b)

