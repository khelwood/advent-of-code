#!/usr/bin/env python3

import sys
import re

def read_preceders():
    A = ord('A')
    ptn = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) ')
    prec = [set() for _ in range(26)]
    succ = [set() for _ in range(26)]
    for line in sys.stdin:
        m = ptn.match(line)
        if not m:
            raise ValueError(repr(line))
        first = ord(m.group(1))-A
        second = ord(m.group(2))-A
        succ[first].add(second)
        prec[second].add(first)
    return prec, succ

def simple_order(prec, succ):
    prec = [set(x) for x in prec]
    succ = [set(x) for x in succ]
    ran = range(26)
    free = {x for x in ran if not prec[x]}
    while free:
        x = next(n for n in ran if n in free)
        yield x
        free.remove(x)
        for z in succ[x]:
            prec[z].remove(x)
            if not prec[z]:
                free.add(z)

class Worker:
    def __init__(self):
        self.time_left = 0
        self.job = None

def threaded_order(prec, succ, num_workers, time_offset=61):
    num_jobs = len(prec)
    ran = range(num_jobs)
    free = {x for x in ran if not prec[x]}
    workers = [Worker() for _ in range(num_workers)]
    jobs_done = []
    ticks = -1
    while len(jobs_done) < num_jobs:
        ticks += 1
        for worker in workers:
            if worker.job is not None:
                worker.time_left -= 1
                if worker.time_left > 0:
                    continue
                job = worker.job
                jobs_done.append(job)
                for z in succ[job]:
                    prec[z].remove(job)
                    if not prec[z]:
                        free.add(z)
                worker.job = None
            x = next((n for n in ran if n in free), None)
            if x is None:
                continue
            free.remove(x)
            worker.job = x
            worker.time_left = x + time_offset
    return ticks

def main():
    A = ord('A')
    prec, succ = read_preceders()
    order = list(simple_order(prec, succ))
    print("Order:", ''.join([chr(A + x) for x in order]))
    t = threaded_order(prec, succ, 5)
    print("Time with 5 workers:", t)

if __name__ == '__main__':
    main()
