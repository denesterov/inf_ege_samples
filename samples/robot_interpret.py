import tkinter as tk
import robot_vm


with open('robot.txt', encoding='utf-8') as f:
    code = robot_vm.Code(f.read())
    code.dump_code()

with open('robot_field.txt', encoding='utf-8') as f:
    field = robot_vm.Field(f.read())

M = robot_vm.Machine(code, field)


WIDTH = 1200
HEIGHT = 800

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(side='top', fill='both', expand=True)

canvas.create_rectangle(50, 50, 1150, 750, fill='lightgray', outline='black')


OUTER_MARGIN = 100
CELL = 50
MARGIN = 5
XOFFSET = 500
CODE_FONT = ('Courier', 12, 'bold')
CODE_LINE_HEIGHT = 16

TIME_STEP = 500

rects = {}
for row in range(field.height):
    for column in range(field.width):
        x1 = XOFFSET + OUTER_MARGIN + column * CELL + MARGIN
        y1 = OUTER_MARGIN + row * CELL + MARGIN
        x2 = x1 + CELL - MARGIN * 2
        y2 = y1 + CELL - MARGIN * 2
        if field.field.get((column, row), '') == 'X':
            fill = 'white'
        else:
            fill = 'darkgray'
        rects[(column, row)] = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='')


robot_arr = None

def draw_robot():
    global robot_arr
    if robot_arr:
        canvas.delete(robot_arr)

    c2 = CELL // 2
    c2m = c2 - MARGIN * 2
    rx, ry = XOFFSET + OUTER_MARGIN + M.x * CELL, OUTER_MARGIN + M.y * CELL
    cx, cy = rx + c2, ry + c2
    dx, dy = M.dir_x * c2m, M.dir_y * c2m

    robot_arr = canvas.create_line(cx - dx, cy - dy, cx + dx, cy + dy, arrow='last', fill='red', width=4)


code_lines = {}
hilited_code_line = None

def draw_code_block(commands, base_indent):
    for c in commands:
        text = f'{c.code_line + 1:2}: {' '*base_indent}{c.cmd}{':' if c.args else ''} {c.args}'
        x = OUTER_MARGIN
        y = OUTER_MARGIN + c.code_line * CODE_LINE_HEIGHT
        code_lines[c.code_line] = canvas.create_text(x, y, text=text, font=CODE_FONT,  justify='left', anchor='nw')
        if c.block:
            draw_code_block(c.block, base_indent + 2)


def update_current_code_line(line_idx:int):
    global hilited_code_line
    if line_idx == hilited_code_line:
        return

    if hilited_code_line in code_lines:
        tk_id = code_lines[hilited_code_line]
        canvas.itemconfigure(tk_id, fill="black")

    if line_idx in code_lines:
        tk_id = code_lines[line_idx]
        canvas.itemconfigure(tk_id, fill="green")

    hilited_code_line = line_idx



def tick():
    if M.is_running:
        print(M.debug_status())
        li = M.get_line_index()
        if li:
            print(f'{li + 1:02}: {code.lines[li]}')
            update_current_code_line(li)

        M.step()
        draw_robot()

        if not M.is_running:
            print(M.debug_status())

    canvas.after(TIME_STEP, tick)


draw_robot()
draw_code_block(code.block, 0)
canvas.after(TIME_STEP, tick)

root.mainloop()
