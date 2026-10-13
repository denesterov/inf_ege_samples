from dataclasses import dataclass
import enum


@dataclass
class Command:
    cmd: str
    args: str
    code_line: int
    block: list = None


class Code:
    def __init__(self, source_code: str):
        self.lines = source_code.splitlines()
        self.block, _ = self._parse_block([s.lower() for s in self.lines], 0, 0)


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


    def dump_code(self):
        self._dump_block(self.block)


class Field:
    DIRS = { 'L': (-1, 0), 'R': (+1, 0), 'U': (0, -1), 'D': (0, +1) }

    def __init__(self, text_data: str):
        lines = text_data.splitlines()
        self.field = {}
        self.bonuses = []
        self.start = None
        self.finish = None
        d = lines[0].strip()
        if d not in Field.DIRS:
            raise Exception(f'Направление может быть только таким: {Field.DIRS}')
        self.start_dir = Field.DIRS[d]

        height, width = 0, 0
        for ln in lines[1:]:
            ln = ln.strip()
            if ln == '':
                break
            for i, c in enumerate(ln):
                xy = (i, height)
                if c == 'S':
                    self.start = xy
                elif c == 'X':
                    self.field[xy] = 'X'
                elif c == 'O':
                    self.bonuses.append(xy)
                elif c == 'E':
                    self.finish = xy

            height += 1
            width = max(width, len(ln))

        if not self.start:
            raise Exception(f'В файле поля не задан старт')

        self.height, self.width = height, width


class Machine:
    CONDITIONS = ('св', 'занято', 'св слева', 'св справа', 'занято слева', 'занято справа')

    @dataclass
    class StackFrame:
        code: list[Command]
        ip: int
        is_cycle: bool

    def __init__(self, code: Code, field: Field):
        self.stack = list[self.StackFrame]()
        self.code = code.block
        self.ip = 0
        self.total_steps = 0
        self.bonus_score = 0

        self.field = field
        (self.x, self.y) = self.field.start
        (self.dir_x, self.dir_y) = self.field.start_dir
        self.bonuses = self.field.bonuses

        self.is_running = True
        self.error_message = None


    def step(self):
        if not self.is_running:
            return

        while self.ip >= len(self.code):
            # end of block
            if len(self.stack) == 0:
                self.is_running = False
                return
            frame = self.stack[-1]
            if frame.is_cycle: # just repeat
                self.ip = 0
                break
            else:
                self.stack.pop()
                self.code = frame.code
                self.ip = frame.ip

        cmd = self.code[self.ip]
        if cmd.cmd == 'шаг':
            if not self._cell_available(self.x + self.dir_x, self.y + self.dir_y):
                self._set_error('Столкновение!')
            else:
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
            while len(self.stack) > 0:
                stack_top = self.stack.pop()
                if stack_top.is_cycle:
                    self.code = stack_top.code # WRONG
                    self.ip = stack_top.ip
                    break
            else:
                self._set_error(f'Команда "выход" без "повтора"')
                return
        elif cmd.cmd == 'если':
            cond = self._check_condition(cmd.args)
            if cond is None:
                self._set_error(f'Неизвестное условие "{cmd.args}"')
                return

            if cond:
                self.stack.append(self.StackFrame(self.code, self.ip + 1, False))
                self.code = cmd.block
                self.ip = 0
            else:
                self.ip += 1
        else:
            self._set_error(f'Неизвестная команда "{cmd.cmd}"')
            return

        self.total_steps += 1

        pos = (self.x, self.y)
        if pos == self.field.finish:
            self.is_running = False

        if pos in self.bonuses:
            self.bonuses.remove(pos)
            self.bonus_score += 1


    def _cell_available(self, x, y):
        if x < 0 or y < 0 or x >= self.field.width or y >= self.field.height:
            return False

        return self.field.field.get((x, y), '') != 'X'


    def _check_condition(self, condition):
        if condition not in Machine.CONDITIONS:
            return None

        dx, dy = (self.dir_x, self.dir_y)
        if 'слева' in condition:
            dx, dy = +dy, -dx
        elif 'справа' in condition:
            dx, dy = -dy, +dx
        inverse = 'занято' in condition

        result = self._cell_available(self.x + dx, self.y + dy)
        return not result if inverse else result


    def _set_error(self, msg):
        self.is_running = False
        self.error_message = msg


    def debug_status(self):
        basics = f'Бонусов: {self.bonus_score}\nPos: ({self.x + 1}, {self.y + 1}), Dir: ({self.dir_x}, {self.dir_y})'

        if self.ip < len(self.code):
            line = self.code[self.ip].code_line + 1
        else:
            if len(self.code) > 0:
                line = f'Behind {self.code[-1].code_line + 1}'
            else:
                line = f'-'

        if self.is_running:
            cond = '\n'.join([f'{c}: {self._check_condition(c)}' for c in Machine.CONDITIONS])
            return f'{basics}, Line: {line}\nSteps: {self.total_steps}, Stack: {len(self.stack)}\nIP: {self.ip} / {len(self.code)}\n{cond}'
        elif self.error_message:
            return f'Ошибка: {self.error_message}\n{basics}, Steps: {self.total_steps}'
        else:
            return f'Финиш!\n{basics}, Steps: {self.total_steps}'


    def get_line_index(self):
        if self.is_running and len(self.code) > 0 and self.ip < len(self.code):
            return self.code[self.ip].code_line
        return None
