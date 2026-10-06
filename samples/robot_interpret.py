from dataclasses import dataclass
import tkinter as tk


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

    def __init__(self, sx: int, sy: int, field: dict[(int, int), str]):
        self.code = []
        self.size_x = sx
        self.size_y = sy
        self.x = sx // 2
        self.y = sy // 2
        self.dir_x = 0
        self.dir_y = 1
        self.field = field
        self.is_running = False

    def start(self, code: list[Command], start_x, start_y):
        self.stack = list[self.StackFrame]()
        self.code = code
        self.ip = 0
        self.x = start_x
        self.y = start_y
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


with open('robot.txt', encoding='utf-8') as f:
    source = f.read()

with open('robot_field.txt', encoding='utf-8') as f:
    field = {}
    fld_height, fld_width = 0, 0
    start_x, start_y = [int(s) for s in f.readline().split()]

    for ln in f:
        ln = ln.strip()
        if ln == '':
            break
        for i, c in enumerate(ln):
            if c == 'X':
                field[(i, fld_height)] = 'X'
        fld_height += 1
        fld_width = max(fld_width, len(ln))


code, ln_idx = parse_block([s.lower() for s in source.splitlines()], 0, 0)
dump_block(code)

M = Machine(fld_width, fld_height, field)
M.start(code, start_x, start_y)


WIDTH = 1200
HEIGHT = 800

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(side='top', fill='both', expand=True)

canvas.create_rectangle(50, 50, 1150, 750, fill='lightgray', outline='black')


OUTER_MARGIN = 100
CELL = 50
MARGIN = 8
TIME_STEP = 500

rects = {}
for row in range(fld_height):
    for column in range(fld_width):
        x1 = OUTER_MARGIN + column * CELL + MARGIN
        y1 = OUTER_MARGIN + row * CELL + MARGIN
        x2 = x1 + CELL - MARGIN
        y2 = y1 + CELL - MARGIN
        if field.get((column, row), '') == 'X':
            fill = 'white'
        else:
            fill = 'darkgray'
        rects[(column, row)] = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='')


robot_arr = None

def draw_robot():
    global robot_arr
    if robot_arr:
        canvas.delete(robot_arr)

    rx = OUTER_MARGIN + M.x * CELL
    ry = OUTER_MARGIN + M.y * CELL

    robot_arr = canvas.create_line(rx + CELL//2, ry + CELL - MARGIN, rx + CELL//2, ry + MARGIN, arrow='last', fill='red', width=2)


draw_robot()


def tick():
    print(f'X: {M.x}, Y: {M.y}, DX: {M.dir_x}, DY: {M.dir_y}, Stack len: {len(M.stack)}, Running: {M.is_running}')
    M.step()
    canvas.after(TIME_STEP, tick)


canvas.after(TIME_STEP, tick)

root.mainloop()
