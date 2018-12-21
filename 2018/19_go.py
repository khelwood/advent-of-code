#!/usr/bin/env python3

import sys

from opfunc import read_commands

# As it turns out, this is the program I was given:
#
# 0: goto 17
# 1:
#   registers[0] += sum of factors of registers[2]
#   end program
# 
# 17:
#  if registers[0]:
#    set registers[2] to some value
#    goto 1
#  else
#    set registers[2] to some other value
#    goto 1
# So if "cheat" is true, we wil come out of the program
#  part way through, and calculate the sum of the factors more practically.
def run(ip, commands, registers, cheat=False):
    num_commands = len(commands)
    while 0 <= registers[ip] < num_commands:
        command = commands[registers[ip]]
        command(registers)
        registers[ip] += 1
        if cheat and registers[ip]==1:
            # If we're cheating, then as soon as
            # we get to line 1, we can calculate the answer.
            registers[0] += sum_factors(registers[2])
            break

def sum_factors(num):
    return num + sum(i for i in range(1, num) if num%i==0)

def main():
    cheat = ('--nocheat' not in sys.argv[1:])
    ip,commands = read_commands(sys.stdin)
    
    registers = [0]*6
    print("Starting with registers[0] =", registers[0])
    run(ip, commands, registers, cheat=cheat)
    print("Register 0:", registers[0])
    registers = [1] + [0]*5
    print("Starting with registers[0] =", registers[0])
    run(ip, commands, registers, cheat=cheat)
    print("Register 0:", registers[0])    

if __name__ == '__main__':
    main()
