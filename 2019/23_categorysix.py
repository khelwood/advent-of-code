#!/usr/bin/env python3

import sys
from intcode import Program, parse_program_input

def create_programs(program_input, queues, nat=None):
    programs = [Program(program_input) for _ in range(50)]
    for i,prog in enumerate(programs):
        prog.queue = queues[i]
        prog.queue.append(i)
        prog.awaiting = False
        def prog_input(p=prog):
            if not p.queue:
                p.awaiting = True
                return -1
            return p.queue.pop(0)
        prog.input_func = prog_input
        def prog_output(value, oc=[]):
            oc.append(value)
            if len(oc)==3:
                prog.awaiting = False
                destination, x, y = oc
                oc.clear()
                q = queues[destination]
                if destination < len(programs):
                    programs[destination].awaiting = False
                if destination==nat:
                    q[:] = [x,y]
                else:
                    q += [x,y]
        prog.output_func = prog_output
    return programs

def part_one(program_input):
    queues = [[] for _ in range(256)]
    programs = create_programs(program_input, queues)
    done = False
    while not done:
        for prog in programs:
            prog.perform_command()
            if len(queues[255]) >= 2:
                done = True
                break
    print("Queue 255:", queues[255])
    
def part_two(program_input):
    queues = [[] for _ in range(256)]
    programs = create_programs(program_input, queues, nat=255)
    nat = queues[255]
    last_nat = None

    while True:
        idle = True
        for prog in programs:
            prog.perform_command()
            if idle and not prog.awaiting:
                idle = False
        if idle and nat:
            queues[0].extend(nat)
            y = nat[1]
            if y==last_nat:
                break
            last_nat = y
            programs[0].awaiting = False
    print("NAT repeated:", last_nat)
    

def main():
    program_input = parse_program_input(sys.stdin.read())
    part_one(program_input)
    part_two(program_input)

if __name__ == '__main__':
    main()
