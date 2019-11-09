# brainfuck-interpreter and debugger

$ python machine.py filename

$ python debugger.py filename

vが示してるのは次実行する文字(ip)

![](https://github.com/Lan-t/brainfuck-debugger/blob/images/screenshot.png)

## command

- s: do step
- sb: do step to breakpoint
- sbb: do step to before breakpoint

- b[number]: set breakpoint at [number]
- bd[number]: unset breakpoint at [number]

- w: write to machine's stdin
- v, vs: save machine snap
- vl[number]: load snap [number]