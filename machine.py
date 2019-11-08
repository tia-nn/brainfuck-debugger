from typing import List, Union
import sys
from collections import deque


class BrainFuckMachine:
    array: List
    _pointer: int
    code: str
    stack: deque
    ip: int
    nf: bool

    stdin: str
    stdin_p: int
    stdout: str

    do_print: bool

    def __init__(self, do_print: bool = True):
        self.array = [0]
        self._pointer = 0
        self.code = ''
        self.stack = deque()
        self.ip = 0
        self.nf = False
        self.stdin = ''
        self.stdin_p = 0
        self._stdout = ''
        self.do_print = do_print

    @property
    def pointer(self):
        return self._pointer

    @pointer.setter
    def pointer(self, p):
        if p == len(self.array):
            self.array.append(0)
        self._pointer = p

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, n):
        if self.do_print:
            print(n[len(self.stdout):], end='')
        self._stdout = n

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

        self.stdout += c

    def read(self):
        if len(self.stdin) == self.stdin_p:
            a = input()
            if not a:
                a = '\n'
            self.stdin += a

        self.array[self.pointer] = ord(self.stdin[self.stdin_p])
        self.stdin_p += 1

    def jz_e(self):
        self.stack.append(self.ip)
        if not self.array[self.pointer]:
            self.nf = True

    def jz_s(self):
        ip = self.stack.pop()
        self.nf = False
        if self.array[self.pointer]:
            self.ip = ip - 1

    def step(self) -> Union[bool, None]:
        if self.ip >= len(self.code):
            return True

        c = self.code[self.ip]

        try:
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

        except KeyError:
            pass

        self.ip += 1
        try:
            while (self.nf and self.code[self.ip] != ']') or (self.code[self.ip] not in '><+-.,[]'):
                self.ip += 1
        except IndexError:
            return True

    def run(self, code):
        self.code = code
        self.ip = 0

        while not self.step():
            pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.stderr.write('usage: python machine.py [filename] [-d --debug]')
        exit(1)

    filename = sys.argv[1]

    machine = BrainFuckMachine()
    machine.run(open(filename).read())
