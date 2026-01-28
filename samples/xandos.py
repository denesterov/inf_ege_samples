import tkinter as tk

field = [[' '] * 3 for _ in range(3)]
next_move = 'X'

root = tk.Tk()
canvas = tk.Canvas(root, width=410, height=310, bg='white')
canvas.pack(side="top", fill="both", expand=True)

for row in range(3):
    for column in range(3):
        x1, y1 = 10 + column * 100, 10 + row * 100
        x2, y2 = x1 + 90, y1 + 90
        canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
text_item = canvas.create_text(310, 30, text='Next: '+ next_move, anchor='w', font=('Arial', 14, 'bold'))

def draw_move(r, c):
    m = field[r][c]
    cx, cy = 10 + c * 100 + 45, 10 + r * 100 + 45
    if m == 'X':
        canvas.create_line(cx - 30, cy - 30, cx + 30, cy + 30)
        canvas.create_line(cx - 30, cy + 30, cx + 30, cy - 30)
    elif m == 'O':
        canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30)

def find_rc_by_xy(x, y):
    r = (y - 10) // 100
    c = (x - 10) // 100
    if r >= 0 and r < 3 and c >= 0 and c < 3:
        return r, c
    return None

def check_victory():
    lines = []
    lines.extend([[(r, c) for r in range(3)] for c in range(3)])
    lines.extend([[(r, c) for c in range(3)] for r in range(3)])
    lines.append([(i, i) for i in range(3)])
    lines.append([(2 - i, i) for i in range(3)])
    for ln in lines:
        moves = [field[r][c] for r, c in ln]
        if all(m in ['X', 'O'] for m in moves) and all(m == moves[0] for m in moves):
            return moves[0]
    return ''

def on_mouse_click(event):
    global next_move
    if next_move == '':
        return

    rc = find_rc_by_xy(event.x, event.y)
    if rc is None:
        return
    r, c = rc
    field[r][c] = next_move
    draw_move(r, c)

    next_move = 'O' if next_move == 'X' else 'X'
    new_text = 'Next: '+ next_move

    V = check_victory()
    if V != '':
        new_text = V + ' wins!'
        next_move = ''

    canvas.itemconfig(text_item, text=new_text)

root.bind('<Button>', on_mouse_click)

root.mainloop()
