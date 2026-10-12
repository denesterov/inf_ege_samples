import tkinter as tk
import robot_vm


with open('robot.txt', encoding='utf-8') as f:
    code = robot_vm.Code(f.read())
    code.dump_code()

with open('robot_field.txt', encoding='utf-8') as f:
    field = robot_vm.Field(f.read())

M = robot_vm.Machine(code, field)

playback_on = False

WIDTH = 1200
HEIGHT = 800
BORDER = 50

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(side='top', fill='both', expand=True)

canvas.create_rectangle(BORDER, BORDER, WIDTH - BORDER, HEIGHT - BORDER, fill='lightgray', outline='black')

OUTER_MARGIN = 20
CELL = 50
MARGIN = 5
XOFFSET = 500
CODE_FONT = ('Courier', 12, 'bold')
CODE_LINE_HEIGHT = 18

TIME_STEP = 500

rects = {}
for row in range(field.height):
    for column in range(field.width):
        x1 = BORDER + XOFFSET + OUTER_MARGIN + column * CELL + MARGIN
        y1 = BORDER + OUTER_MARGIN + row * CELL + MARGIN
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
    rx, ry = BORDER + XOFFSET + OUTER_MARGIN + M.x * CELL, BORDER + OUTER_MARGIN + M.y * CELL
    cx, cy = rx + c2, ry + c2
    dx, dy = M.dir_x * c2m, M.dir_y * c2m

    robot_arr = canvas.create_line(cx - dx, cy - dy, cx + dx, cy + dy, arrow='last', fill='red', width=4)


code_lines = {}
hilited_code_line = None

def draw_code_block(commands, base_indent):
    for c in commands:
        text = f'{c.code_line + 1:2}: {' '*base_indent}{c.cmd}{':' if c.args else ''} {c.args}'
        x = BORDER + OUTER_MARGIN
        y = BORDER + OUTER_MARGIN + c.code_line * CODE_LINE_HEIGHT
        code_lines[c.code_line] = canvas.create_text(x, y, text=text, font=CODE_FONT,  justify='left', anchor='nw')
        if c.block:
            draw_code_block(c.block, base_indent + 2)


def update_current_code_line():
    global hilited_code_line

    line_idx = M.get_line_index()
    if line_idx:
        print(f'{line_idx + 1:02}: {code.lines[line_idx]}')

    if line_idx == hilited_code_line:
        return

    if hilited_code_line in code_lines:
        tk_id = code_lines[hilited_code_line]
        canvas.itemconfigure(tk_id, fill="black")

    if line_idx in code_lines:
        tk_id = code_lines[line_idx]
        canvas.itemconfigure(tk_id, fill="blue")

    hilited_code_line = line_idx



text_status = []

def draw_status():
    global text_status

    for id in text_status:
        canvas.delete(id)
    text_status = []

    x = BORDER + OUTER_MARGIN + XOFFSET
    y = BORDER + OUTER_MARGIN + CELL * field.height + OUTER_MARGIN

    text = M.debug_status()
    text_status.append(canvas.create_text(x, y, text=text, font=CODE_FONT,  justify='left', anchor='nw'))


def execute_one_step():
    if not M.is_running:
        return False

    M.step()
    draw_robot()
    draw_status()
    update_current_code_line()
    return True


def tick():
    if playback_on:
        execute_one_step()

    canvas.after(TIME_STEP, tick)


def on_button_startstop():
    global playback_on  
    playback_on = not playback_on

buttons_startstop = tk.Button(root, text="Start / Pause", command=on_button_startstop)
canvas.create_window(BORDER + OUTER_MARGIN, HEIGHT - BORDER - OUTER_MARGIN, window=buttons_startstop, anchor="sw")


def on_button_one_step():
    if not execute_one_step():
        print('Finished')


button_onestep = tk.Button(root, text="Single Step", command=on_button_one_step)
canvas.create_window(BORDER + OUTER_MARGIN + 100, HEIGHT - BORDER - OUTER_MARGIN, window=button_onestep, anchor="sw")


def on_button_restart():
    global M
    M = robot_vm.Machine(code, field)
    draw_robot()
    draw_status()
    draw_code_block(code.block, 0)
    update_current_code_line()

button_onestep = tk.Button(root, text="Restart", command=on_button_restart)
canvas.create_window(BORDER + OUTER_MARGIN + 200, HEIGHT - BORDER - OUTER_MARGIN, window=button_onestep, anchor="sw")

draw_robot()
draw_status()
draw_code_block(code.block, 0)
update_current_code_line()

canvas.after(TIME_STEP, tick)

root.mainloop()
