#!/usr/bin/env python3

import sys
import importlib

leo = importlib.import_module('12_leo')

TOGGLE_PTN = leo._compile('tgl #')

def analyse_copy(line):
    m = leo._match(leo.COPY_PTN, line)
    return m.group(1), m.group(2)

def analyse_alter(line):
    m = leo._match(leo.ALTER_PTN, line)
    delta = 1 if m.group(1)=='inc' else -1
    return m.group(2), delta

def analyse_jump(line):
    m = leo._match(leo.JUMP_PTN, line)
    return m.group(1), m.group(2)

class Togram(leo.Program):
    def process(self, line):
        k = sorted(self.registers)
        print(" Line: %s   "%self.position, end='\r')
        if line.startswith('tgl'):
            return self.process_toggle(line)
        return super().process(line)
    def process_toggle(self, line):
        m = leo._match(TOGGLE_PTN, line)
        arg = m.group(1)
        target_line = self.position + self[arg]
        if 0<=target_line<len(self.lines):
            old_line = self.lines[target_line]
            new_line = self.toggle(old_line)
            print("Toggle %r -> %r"%(old_line, new_line))
            self.lines[target_line] = new_line
        self.advance()
    def toggle(self, line):
        if line.startswith('inc'):
            return 'dec' + line[3:]
        if line.startswith('dec') or line.startswith('tgl'):
            return 'inc' + line[3:]
        if line.startswith('jnz'):
            return 'cpy' + line[3:]
        return 'jnz' + line[3:]
    def unwrap(self, src, delta):
        if delta==-5 and self.unwrap_five(src, self.position+delta):
            return True
        return super().unwrap(src, delta)
    def unwrap_five(self, src, start):
        """The described pattern of 5 lines plus a jump backwards
        produces what amounts to a multiplication using nested for loops."""
        lines = self.lines[start:start+5]
        if not (lines[0].startswith('cpy')
                and (lines[1].startswith('inc') or lines[1].startswith('dec'))
                and (lines[2].startswith('inc') or lines[2].startswith('dec'))
                and lines[3].startswith('jnz')
                and lines[4].startswith('inc') or lines[4].startswith('dec')):
            return False
        a_src, a_dst = analyse_copy(lines[0])
        b_target, b_delta = analyse_alter(lines[1])
        c_target, c_delta = analyse_alter(lines[2])
        d_test, d_delta = analyse_jump(lines[3])
        e_target, e_delta = analyse_alter(lines[4])
        if not (a_dst==c_target==d_test
                and len({a_src, a_dst, b_target, e_target})==4):
            return False
        self[b_target] += b_delta * self[a_src] * self[e_target]
        self[e_target] = 0
        self[c_target] = 0
        return True

def main():
    if len(sys.argv) <= 1:
        exit("Usage: %s <number>"%sys.argv[0])
    start = int(sys.argv[1])
    lines = sys.stdin.read().strip().split('\n')
    prog = Togram(lines)
    prog['a'] = start
    print("Running...")
    prog.run()
    print(f"prog['a']=={prog['a']}")

    
if __name__ == '__main__':
    main()
