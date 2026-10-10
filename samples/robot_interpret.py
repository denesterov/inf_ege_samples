from dataclasses import dataclass
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
MARGIN = 8
TIME_STEP = 500

rects = {}
for row in range(field.height):
    for column in range(field.width):
        x1 = OUTER_MARGIN + column * CELL + MARGIN
        y1 = OUTER_MARGIN + row * CELL + MARGIN
        x2 = x1 + CELL - MARGIN
        y2 = y1 + CELL - MARGIN
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

    rx = OUTER_MARGIN + M.x * CELL
    ry = OUTER_MARGIN + M.y * CELL

    robot_arr = canvas.create_line(rx + CELL//2, ry + CELL - MARGIN, rx + CELL//2, ry + MARGIN, arrow='last', fill='red', width=2)


draw_robot()


def tick():
    if M.is_running:
        M.step()
        print(M.debug_status())

        if M.is_running:
            li = M.get_line_index()
            if li:
                print(f'{li + 1:02}: {code.lines[li]}')

    canvas.after(TIME_STEP, tick)


canvas.after(TIME_STEP, tick)

root.mainloop()
