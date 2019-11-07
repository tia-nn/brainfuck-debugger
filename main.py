from typing import List
import sys
from collections import deque
from itertools import zip_longest
import os


class BrainFuckMachine:
    array: List
    _pointer: int
    code: str
    stack: deque
    ip: int
    nf: bool

    debug: bool
    debug_stdout: str

    def __init__(self, debug: bool = False):
        self.array = [0]
        self._pointer = 0
        self.code = ''
        self.stack = deque()
        self.ip = 0
        self.nf = False
        self.debug = debug
        self.debug_stdout = ''

    @property
    def pointer(self):
        return self._pointer

    @pointer.setter
    def pointer(self, p):
        if p == len(self.array):
            self.array.append(0)
        self._pointer = p

    def p_inc(self):
        self.pointer += 1

    def p_dec(self):
        self.pointer = self.pointer - 1

    def inc(self):
        self.array[self.pointer] += 1

    def dec(self):
        self.array[self.pointer] -= 1

    def put(self):
        c = chr(self.array[self.pointer])

        if self.debug:
            self.debug_stdout += c
        else:
            print(c, end='')

    def read(self):
        self.array[self.pointer] = ord(sys.stdin.read(2)[0])

    def jz_e(self):
        self.stack.append(self.ip)
        if not self.array[self.pointer]:
            self.nf = True

    def jz_s(self):
        ip = self.stack.pop()
        self.nf = False
        if self.array[self.pointer]:
            self.ip = ip - 1

    def step(self):
        c = self.code[self.ip]

        if c not in '><+-.,[]':
            self.ip += 1
            return

        if self.nf and c != ']':
            self.ip += 1
            return

        if self.debug:
            self.put_state()
            input()

        {
            '>': self.p_inc,
            '<': self.p_dec,
            '+': self.inc,
            '-': self.dec,
            '.': self.put,
            ',': self.read,
            '[': self.jz_e,
            ']': self.jz_s,
        }[c]()

        self.ip += 1

    def run(self, code):
        self.code = code
        self.ip = 0

        while True:
            try:
                self.step()
            except IndexError:
                break

        if self.debug:
            self.put_state()
            input()

    def put_state(self):
        os.system('clear')

        put_table = [
                        *(('', ''),) * 2 * (self.ip // 30),
                        ('array:', self.array),
                        ('pointer:', self.pointer),
                        ('stack:', self.stack),
                        ('ip:', self.ip)
                    ]

        put_code = []
        for i, v in enumerate([self.code[i:i + 30] for i in range(0, len(self.code), 30)]):
            if i == self.ip // 30:
                a = self.ip % 30
                put_code.append(' ' * (a + a // 10) + 'v')

            put_code.append(v[:10] + ' ' + v[10:20] + ' ' + v[20:30])
            put_code.append('0123456789 0123456789 0123456789')

        put = zip_longest(put_code, put_table, fillvalue='')

        for i in put:
            i0 = i[0] or ''
            i1 = i[1] or ('', '')
            print('{:32}'.format(i0), i1[0], i1[1])

        print()
        print('stdout:', self.debug_stdout)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.stderr.write('usage: python main.py [filename] [-d --debug]')

    filename = sys.argv[1]
    try:
        deb = bool(sys.argv[2])
    except IndexError:
        deb = False

    machine = BrainFuckMachine(deb)
    machine.run(open(filename).read())

    # code = '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+.+.>++++++++++.'
    # code2 = '+++++++++[>++++++++>+++++++++++>+++>+<<<<-]>.>++.+++++++..+++.>+++++.<<+++++++++++++++.>.+++.------.--------.>+.>+.'
    # code3 = '+-[+++]++++++++++[>++++++++++<-]>.'
    # machine.run(code3)