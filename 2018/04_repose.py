#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

TIMEFORMAT = '%Y-%m-%d %H:%M'

@dataclass
class Guard:
    id: int
    shifts: list = field(default_factory=list)
    def sleepiness(self):
        return sum(map(Shift.sleeptime, self.shifts))
    def sleepiest_minute(self):
        minutes = [0]*60
        for shift in self.shifts:
            for sleep in shift.sleeps:
                for m in sleep:
                    minutes[m] += 1
        most = max(minutes)
        return most, minutes.index(most)

@dataclass
class Shift:
    date: date
    sleeps: list = field(default_factory=list)
    def __repr__(self):
        sleepdescs = ', '.join([f"({s.start}-{s.stop})" for s in self.sleeps])
        return f"({self.date}: [{sleepdescs}]"
    def sleeptime(self):
        return sum(map(len, self.sleeps))

SHIFT_PTN=re.compile(r'guard #(\d+) begins shift')

def read_history():
    lines = sorted(sys.stdin.read().strip().splitlines())
    guards = {}
    start = None
    for line in lines:
        assert line[0]=='['
        ts, _, desc = line[1:].partition(']')
        ts = datetime.strptime(ts, TIMEFORMAT)
        date = ts.date()
        if ts.hour!=0:
            date += timedelta(days=1)
        desc = desc.strip().lower()
        if desc=='falls asleep':
            if date!=shift.date:
                print("Shift:", shift)
                print("Line:", line)
                assert False
            assert date==shift.date
            start = ts.minute
            continue
        if desc=='wakes up':
            if date!=shift.date:
                print("Shift:", shift)
                print("Line:", line)
                assert False
            shift.sleeps.append(range(start, ts.minute))
            start = None
            continue
        m = SHIFT_PTN.match(desc)
        if not m:
            raise ValueError(repr(line))
        assert start is None
        guard_id = int(m.group(1))
        if guard_id in guards:
            guard = guards[guard_id]
        else:
            guard = Guard(guard_id)
            guards[guard_id] = guard
        shift = Shift(date)
        guard.shifts.append(shift)
    assert start is None
    return sorted(guards.values(), key=lambda g:g.id)

def main():
    guards = read_history()
    sleepiest = max(guards, key=Guard.sleepiness)
    _, minute = sleepiest.sleepiest_minute()
    print(f"Guard {sleepiest.id} slept the most at minute {minute}.")
    print("Product:", sleepiest.id * minute)
    print()
    most_sleeps = 0
    for guard in guards:
        sleeps, minute = guard.sleepiest_minute()
        if sleeps > most_sleeps:
            most_sleeps = sleeps
            sleepiest = guard
            sleepiest_minute = minute
    print(f"Guard {sleepiest.id} was asleep {most_sleeps} times "
              f"at minute {sleepiest_minute}.")
    print("Product:", sleepiest.id * sleepiest_minute)

if __name__ == '__main__':
    main()
