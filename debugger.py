from typing import List, Set
import os
import sys
from itertools import zip_longest
from string import whitespace
from collections import defaultdict

from machine import BrainFuckMachine
from color import COLOR


class Debugger:
    machine: BrainFuckMachine
    snaps: List[BrainFuckMachine]
    breakpoints: Set[int]
    is_ended: bool

    def __init__(self, code):
        self.machine = BrainFuckMachine(False)
        self.machine.code = code
        self.snaps = []
        self.breakpoints = set()
        self.is_ended = False

    def set_break(self, p):
        if p >= len(self.machine.code):
            return False
        self.breakpoints.add(p)

    def remove_break(self, p):
        self.breakpoints.remove(p)

    def step(self):
        self.is_ended = self.machine.step()
        return self.is_ended

    def put_state(self, n: int = 6, snap=None):
        machine = snap or self.machine
        code = machine.code
        for i in whitespace:
            code = code.replace(i, ' ')

        put_str = []
        for i, v in enumerate([code[i:i + 10*n] for i in range(0, len(code), 10*n)]):
            if i == machine.ip // (10*n):
                a = machine.ip % (10*n)
                put_str.append(('{:%d}' % (11*n-1)).format(' ' * (a + a // 10) + 'v'))
            else:
                put_str.append(' ' * (11*n-1))

            b = ''
            for i in range(0, 10*n, 10):
                b += v[i:i+10] + ' '
            put_str.append(('{:%d}' % (11*n-1)).format(b))
            put_str.append('0123456789 ' * n)

        put_str.append('')

        put_str.append('array:      %s' % machine.array)
        put_str.append('pointer:    %s' % machine.pointer)
        put_str.append('stack:      %s' % machine.stack)
        put_str.append('ip:         %s' % machine.ip)

        put_str.append('')
        put_str.append('breaks:     %s' % self.breakpoints)
        put_str.append('')

        put_str.append('stdout:     %s' % machine.stdout)
        put_str.append('stdin:      %s' % machine.stdin)
        put_str.append('            %s' % (' ' * machine.stdin_p + 'A'))

        os.system('clear')
        for i in sorted(self.breakpoints, key=lambda x: -x):
            row = i // (10 * n) * 3 + 1
            col = i % (10 * n)
            col += col // 10
            s = put_str[row]
            c = s[col]
            s = s[:col] + COLOR.CYAN + c + COLOR.END + s[col+1:]
            put_str[row] = s

        for i in put_str:
            print(i)

    def repl(self):
        while True:
            self.put_state()
            print('>> ', end='')
            a = input()

            while not a:
                self.put_state()
                print('>> ', end='')
                a = input()

            if a[0] == 's':
                if len(a) == 1:
                    if self.step(): return
                elif a[1] == 'b':
                    if len(a) == 2:
                        while self.machine.ip not in self.breakpoints:
                            if self.step():
                                self.put_state()
                                return
                        if self.step():
                            self.put_state()
                            return
                    elif a[2] == 'b':
                        while self.machine.ip+1 not in self.breakpoints:
                            if self.step():
                                self.put_state()
                                return
                        if self.step():
                            self.put_state()
                            return

            elif a[0] == 'b':
                if a[1] == 'd':
                    self.remove_break(int(a[2:]))
                else:
                    self.set_break(int(a[1:]))

            elif a[0] == 'w':
                print('stdin << ', end='')
                a = input()
                if not a:
                    a = '\n'
                self.machine.stdin += a

            elif a[0] == '.':
                return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.stderr.write('usage: python machine.py [filename] [-d --debug]')
        exit(1)

    filename = sys.argv[1]

    debugger = Debugger(open(filename).read())

    debugger.repl()
