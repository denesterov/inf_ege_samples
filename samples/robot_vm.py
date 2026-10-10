from dataclasses import dataclass
import tkinter as tk


@dataclass
class Command:
    cmd: str
    args: str
    code_line: int
    block: list = None


class Code:
    def __init__(self, source_code: str):
        self.block, _ = self._parse_block([s.lower() for s in source_code.splitlines()], 0, 0)
        self._dump_block(self.block)


    def _parse_block(self, source: list[str], block_indent, start_line):
        block = list[Command]()

        ln_idx = start_line
        while ln_idx < len(source):
            ln = source[ln_idx]
            lnstr = ln.strip()

            if len(lnstr) == 0 or lnstr[0] == '#':
                ln_idx += 1
                continue

            indent = len(ln) - len(ln.lstrip())
            if indent < block_indent:
                return block, ln_idx
            if indent > block_indent:
                raise Exception(f'Line {start_line + ln_idx}: Expecting indent {block_indent}, got {indent}')

            words = ln.split()
            args = ' '.join(words[1:])
            cmd = Command(words[0], args, ln_idx)

            if cmd.cmd == 'если' or cmd.cmd == 'повтор':
                cmd.block, ln_idx = self._parse_block(source, block_indent + 2, ln_idx + 1)
            else:
                ln_idx += 1

            block.append(cmd)

        return block, ln_idx


    def _dump_block(self, commands: list[Command], base_indent = 0):
        for c in commands:
            print(f'{c.code_line + 1:02}:{' '*base_indent}{c.cmd}{':' if c.args else ''} {c.args}')
            if c.block:
                self._dump_block(c.block, base_indent + 2)


class Field:
    def __init__(self, text_data: str):
        lines = text_data.splitlines()
        self.field = {}
        self.start_x, self.start_y = [int(s) for s in lines[0].split()]

        height, width = 0, 0
        for ln in lines[1:]:
            ln = ln.strip()
            if ln == '':
                break
            for i, c in enumerate(ln):
                if c == 'X':
                    self.field[(i, height)] = 'X'
            height += 1
            width = max(width, len(ln))

        self.height, self.width = height, width


class Machine:
    @dataclass
    class StackFrame:
        code: list[Command]
        ip: int
        is_cycle: bool

    def __init__(self, field: Field):
        self.code = []
        self.x = 0
        self.y = 0
        self.dir_x = 0
        self.dir_y = 1
        self.field = field
        self.is_running = False

    def start(self, code: Code):
        self.stack = list[self.StackFrame]()
        self.code = code.block
        self.ip = 0
        self.x = self.field.start_x
        self.y = self.field.start_y
        self.is_running = True

    def step(self):
        if not self.is_running:
            return
        if self.ip >= len(self.code):
            # end of block
            if len(self.stack) == 0:
                self.is_running = False
                return
            frame = self.stack[-1]
            if frame.is_cycle: # just repeat
                self.ip = 0
            else:
                self.stack.pop()
                self.code = frame.code
                self.ip = frame.ip

        cmd = self.code[self.ip]
        if cmd.cmd == 'шаг':
            self.x += self.dir_x
            self.y += self.dir_y
            self.ip += 1
        elif cmd.cmd == 'лево':
            self.dir_x, self.dir_y = self.dir_y, -self.dir_x
            self.ip += 1
        elif cmd.cmd == 'право':
            self.dir_x, self.dir_y = -self.dir_y, self.dir_x
            self.ip += 1
        elif cmd.cmd == 'повтор':
            self.stack.append(self.StackFrame(self.code, self.ip + 1, True))
            self.code = cmd.block
            self.ip = 0
        elif cmd.cmd == 'выход':
            # TODO
            while len(self.stack) > 0:
                if self.stack[-1].is_cycle:
                    self.code = self.stack[-1].code # WRONG
                    self.ip = self.stack[-1].ip
                self.stack.pop()
        elif cmd.cmd == 'если':
            if cmd.args == 'св':
                test = (self.x + self.dir_x, self.y + self.dir_y)
                if self.field.get(test, '') != 'X':
                    self.stack.append(self.StackFrame(self.code, self.ip + 1, False))
                    self.code = cmd.block
                    self.ip = 0
                else:
                    self.ip += 1
