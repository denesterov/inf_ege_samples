import tkinter as tk
import math
import importlib
nn = importlib.import_module('nn-playg-nn')
box = importlib.import_module('nn-playg-box')


WIDTH, HEIGHT = 1500, 750
X0, Y0 = -10.0, -10.0
X1, Y1 = 130.0, 60.0

root = tk.Tk()
root.geometry(f'{WIDTH}x{HEIGHT}+20+20')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black',)
canvas.pack(side="top", fill="both", expand=True)

debug_texts = {}
debug_texts_tkid = None


def on_button_learn():
    global learn_gen_index
    if learn_gen_index != 0: return
    learn_gen_index = 1
    canvas.after(10, tick_learning)
    debug_text('_status', 'Status: Learning')

def on_button_place_target():
    global placing_target, tracing_mode
    if learn_gen_index != 0: return
    placing_target = True
    tracing_mode = False
    debug_text('_status', 'Status: Place new target')

def on_button_trace_mode():
    global placing_target, tracing_mode
    if learn_gen_index != 0: return
    placing_target = False
    tracing_mode = True
    debug_text('_status', 'Status: Tracing')


button_learn = tk.Button(canvas, text="Start Learning", bg="gray", command=on_button_learn)
canvas.create_window(10, 10, window=button_learn, anchor="nw")
button_place_target = tk.Button(canvas, text="Place Target", bg="gray", command=on_button_place_target)
canvas.create_window(10, 45, window=button_place_target, anchor="nw")
button_trace_mode = tk.Button(canvas, text="Trace Test", bg="gray", command=on_button_trace_mode)
canvas.create_window(10, 80, window=button_trace_mode, anchor="nw")


def on_mouse_click(event):
    global target_pos, target_tkid, placing_target, tracing_mode
    if learn_gen_index != 0:
        return
    if placing_target:
        x, y = from_screen(event.x, event.y)
        target_pos = (x, y)
        canvas.delete(target_tkid)
        target_tkid = draw_circle(*target_pos, target_radius, 'red', 'white')
        placing_target = False
        debug_text('_status', 'Status: Trace')
    if tracing_mode:
        debug_text('_status', 'Status: Idle')
        tracing_mode = False

root.bind('<Button-1>', on_mouse_click)


def on_mouse_move(event):
    global tracing_mode, trace_traj_tkid, trace_target_tkid
    if tracing_mode:
        if trace_traj_tkid is not None: canvas.delete(trace_traj_tkid)
        if trace_target_tkid is not None: canvas.delete(trace_target_tkid)

        x, y = from_screen(event.x, event.y)

        test_res = nn.calc_forward((x, y))
        _, _, _, traj = trace(source, test_res, (x, y))
        trace_traj_tkid = draw_path(traj, 'yellow')
        trace_target_tkid = draw_circle(x, y, target_radius, '', 'yellow')

root.bind('<Motion>', on_mouse_move)


def to_screen(x, y):
    return WIDTH * (x - X0) / (X1 - X0), HEIGHT - HEIGHT * (y - Y0) / (Y1 - Y0)

def to_screen_vec(x, y):
    return WIDTH * x / (X1 - X0), HEIGHT * y / (Y1 - Y0)

def from_screen(sx, sy):
    return X0 + sx / WIDTH * (X1 - X0), Y0 + (HEIGHT - sy) / HEIGHT * (Y1 - Y0)

def draw_circle(x, y, r, fill, outline):
    return canvas.create_oval(*to_screen(x - r, y - r), *to_screen(x + r, y + r), outline=outline, fill=fill)

def draw_line(p1, p2, color):
    return canvas.create_line(*to_screen(*p1), *to_screen(*p2), fill=color)

def draw_path(points, color):
    return canvas.create_line([to_screen(x, y) for x, y in points], fill=color)

def debug_text(id, text):
    global debug_texts_tkid
    debug_texts[id] = text
    if debug_texts_tkid is not None:
        canvas.delete(debug_texts_tkid)
    debug_texts_tkid = canvas.create_text(10, 100, text='\n'.join(debug_texts.values()),
                                          fill='green', font=("Arial", 16, "bold"), justify='left', anchor='nw')

def trace(source, vel, target):
    x, y = source[0], source[1]
    ax, ay = 0.0, -9.81
    vx, vy = vel
    t = 0.0
    dt = 0.05
    travel = 0.0
    hist = [(x, y)]
    min_tgt_dist = math.dist((x, y), target)
    while y >= 0.0 and t < 10.0:
        vx += ax * dt
        vy += ay * dt
        dx, dy = vx * dt, vy * dt
        x += dx
        y += dy
        travel += math.sqrt(dx * dx + dy * dy)

        for box in boxes:
            _, x, y, vx, vy = box.point_collide(x, y, vx, vy)

        tgt_dist = math.dist(target, (x, y))
        min_tgt_dist = min(min_tgt_dist, tgt_dist)
        if tgt_dist < target_radius:
            return True, 0, travel, hist

        if math.dist(hist[-1], (x, y)) >= 0.5:
            hist.append((x, y))

    return False, min_tgt_dist - target_radius, travel, hist


boxes = [
    box.Box(30, 20, 50, 25),
    box.Box(50, 20, 55, 40),
]

target_pos = (40.0, 30.0)
target_radius = 2.0
target_tkid = None
trace_traj_tkid, trace_target_tkid = None, None
source = (0.0, 0.0)

for box in boxes:
    box.draw(canvas, to_screen)


target_tkid = draw_circle(*target_pos, target_radius, 'red', 'white')
draw_line((source[0] - 2.0, source[1]), (source[0] + 2.0, source[1]), 'white')
draw_line((source[0], source[1] - 2.0), (source[0], source[1] + 2.0), 'white')


placing_target = False
tracing_mode = False

nn = nn.Net()
traj_hist = []
learn_gen_index = 0
MAX_GENS = 50

def tick_learning():
    global nn, traj_hist, learn_gen_index

    if learn_gen_index <= MAX_GENS:
        canvas.after(50, tick_learning)
    else:
        learn_gen_index = 0
        debug_text('_status', 'Status: Idle')
        return

    nn.draw_weights(canvas, WIDTH, HEIGHT)

    best_try = None
    best_fun = 0.0
    best_traj, best_out = None, None
    for i in range(20):
        distortion = 0.1 if i >= 10 else 1.0 # todo: make smaller disortions when we are closer to our target
        nn2 = nn.make_distorted_copy(distortion)
        out2 = nn2.calc_forward(target_pos)
        hit, min_dist, travel, traj = trace(source, out2, target_pos)

        target_fun = min_dist + travel * 0.1
        if best_try is None or target_fun < best_fun:
            best_try = nn2
            best_fun = target_fun
            best_traj = traj
            best_out = out2


    debug_text('learning_status', f'Gen {learn_gen_index}: target_fun {best_fun:.2f}, out: {best_out}')
    if len(best_traj) > 1:
        traj_hist.append(draw_path(best_traj, 'gray'))
    if len(traj_hist) > 30:
        canvas.delete(traj_hist[0])
        traj_hist = traj_hist[1:]

    nn = best_try
    learn_gen_index += 1


root.mainloop()
