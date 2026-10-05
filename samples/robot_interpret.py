from dataclasses import dataclass

source = '''
шаг
шаг
если св
  шаг
повтор
  если занято
    выход
  шаг
'''

# если св слева
# если св справа
# если св

@dataclass
class Command:
    cmd: str
    args: str
    block: list = None

def parse_block(source: list[str], block_indent, start_line):
    block = list[Command]()

    ln_idx = start_line
    while ln_idx < len(source):
        ln = source[ln_idx]

        if len(ln.strip()) == 0:
            ln_idx += 1
            continue

        indent = len(ln) - len(ln.lstrip())
        if indent < block_indent:
            return block, ln_idx
        if indent > block_indent:
            raise Exception(f'Line {start_line + ln_idx}: Expecting indent {block_indent}, got {indent}')

        words = ln.split()
        args = ' '.join(words[1:])
        cmd = Command(words[0], args)

        if cmd.cmd == 'если' or cmd.cmd == 'повтор':
            cmd.block, ln_idx = parse_block(source, block_indent + 2, ln_idx + 1)
        else:
            ln_idx += 1

        block.append(cmd)

    return block, ln_idx


def dump_block(commands: list[Command], base_indent = 0):
    for c in commands:
        print(f'{' '*base_indent}{c.cmd}: {c.args}')
        if c.block:
            dump_block(c.block, base_indent + 2)


class Machine:
    @dataclass
    class StackFrame:
        code: list[Command]
        ip: int
        is_cycle: bool

    def __init__(self, sx: int, sy: int):
        self.code = []
        self.size_x = sx
        self.size_y = sy
        self.x = sx // 2
        self.y = sy // 2
        self.dir_x = 0
        self.dir_y = 1
        self.field = dict()
        self.is_running = False

    def start(self, code: list[Command]):
        self.stack = list[self.StackFrame]()
        self.code = code
        self.ip = 0
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

        cmd = code[self.ip]
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


code, ln_idx = parse_block([s.lower() for s in source.splitlines()], 0, 0)
dump_block(code)

m = Machine(10, 10)
m.start(code)

for i in range(10):
    print(f'X: {m.x}, Y: {m.y}, DX: {m.dir_x}, DY: {m.dir_y}, Stack len: {len(m.stack)}')
    m.step()
