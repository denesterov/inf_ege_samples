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

OUTER_MARGIN = 20
CELL = 50
MARGIN = 5
MARGIN_O = 10
XOFFSET = 500
CODE_FONT = ('Courier', 12, 'bold')
CODE_LINE_HEIGHT = 18

TIME_STEP = 500
TIME_STEP_FAST = 100


root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(side='top', fill='both', expand=True)

canvas.create_rectangle(BORDER, BORDER, WIDTH - BORDER, HEIGHT - BORDER, fill='lightgray', outline='black')


def _get_cell_rect(ix, iy, margin = MARGIN):
    x1 = BORDER + XOFFSET + OUTER_MARGIN + ix * CELL + margin
    y1 = BORDER + OUTER_MARGIN + iy * CELL + margin
    x2 = x1 + CELL - margin * 2
    y2 = y1 + CELL - margin * 2
    return (x1, y1, x2, y2)


def _get_cell_center(ix, iy):
    x1, y1, x2, y2 = _get_cell_rect(ix, iy)
    return (x1 + x2) // 2, (y1 + y2) // 2


field_vis = {}
def draw_field():
    global field_vis
    for row in range(field.height):
        for column in range(field.width):
            rect = _get_cell_rect(column, row)
            if field.field.get((column, row), '') == 'X':
                fill = 'white'
            else:
                fill = 'darkgray'
            field_vis[(column, row)] = canvas.create_rectangle(*rect, fill=fill, outline='')

    field_vis['S'] = canvas.create_oval(*_get_cell_rect(*field.start, MARGIN_O), fill='grey20', outline='')
    if field.finish:
        field_vis['F'] = canvas.create_oval(*_get_cell_rect(*field.finish, MARGIN_O), fill='red', outline='')

    draw_bonuses()


def draw_bonuses():
    global field_vis

    for id, tk_id in field_vis.items():
        if type(id) is str and id.startswith('Bonus'):
            canvas.delete(tk_id)

    for i, bonus in enumerate(field.bonuses):
        field_vis[f'Bonus{i}'] = canvas.create_oval(*_get_cell_rect(*bonus, MARGIN_O), fill='orange', outline='')


draw_field()


robot_arr = None
robot_trace = []
robot_last_pos = None


def _add_robot_visual(x, y, dx, dy, trace=False):
    c2m = CELL // 2 - MARGIN_O
    cx, cy = _get_cell_center(x, y)
    dx, dy = dx * c2m, dy * c2m

    color = 'light green' if trace else 'green'
    width = 3 if trace else 6
    return canvas.create_line(cx - dx, cy - dy, cx + dx, cy + dy, arrow='last', fill=color, width=width)


def draw_robot():
    global robot_arr
    if robot_arr:
        canvas.delete(robot_arr)

    global robot_last_pos, robot_trace
    pos = (M.x, M.y, M.dir_x, M.dir_y)
    if robot_last_pos != pos:
        if robot_last_pos:
            robot_trace.append(_add_robot_visual(*robot_last_pos, True))
        robot_last_pos = pos

    robot_arr = _add_robot_visual(*pos)

    for tk_id in robot_trace[:-10]:
        canvas.delete(tk_id)
    if len(robot_trace) >= 10:
        robot_trace = robot_trace[-10:]


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
    color = 'red' if M.error_message else 'black'
    text_status.append(canvas.create_text(x, y, text=text, fill=color, font=CODE_FONT,  justify='left', anchor='nw'))


def execute_one_step():
    if not M.is_running:
        return False

    M.step()
    draw_robot()
    draw_bonuses()
    draw_status()
    update_current_code_line()
    return True


def tick():
    if playback_on:
        execute_one_step()

    canvas.after(TIME_STEP_FAST if button_speed_var.get() else TIME_STEP, tick)


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
    global playback_on
    playback_on = False
    M = robot_vm.Machine(code, field)
    draw_robot()
    draw_status()
    draw_code_block(code.block, 0)
    update_current_code_line()

button_onestep = tk.Button(root, text="Restart", command=on_button_restart)
canvas.create_window(BORDER + OUTER_MARGIN + 200, HEIGHT - BORDER - OUTER_MARGIN, window=button_onestep, anchor="sw")


button_speed_var = tk.IntVar()
button_speed = tk.Checkbutton(root, text="Faster", variable=button_speed_var)
canvas.create_window(BORDER + OUTER_MARGIN + 300, HEIGHT - BORDER - OUTER_MARGIN, window=button_speed, anchor="sw")


draw_robot()
draw_status()
draw_code_block(code.block, 0)
update_current_code_line()

canvas.after(TIME_STEP, tick)

root.mainloop()
