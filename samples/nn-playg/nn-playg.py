import tkinter as tk
import math
import random
import importlib
nn = importlib.import_module('nn-playg-nn')


WIDTH, HEIGHT = 1200, 700
X0, Y0 = -10.0, -10.0
X1, Y1 = 110.0, 60.0

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack(side="top", fill="both", expand=True)

def to_screen(x, y):
    return WIDTH * (x - X0) / (X1 - X0), HEIGHT - HEIGHT * (y - Y0) / (Y1 - Y0)

def to_screen_vec(x, y):
    return WIDTH * x / (X1 - X0), HEIGHT * y / (Y1 - Y0)

def draw_circle(x, y, r, fill, outline):
    return canvas.create_oval(*to_screen(x - r, y - r), *to_screen(x + r, y + r), outline=outline, fill=fill)

def draw_line(p1, p2, color):
    return canvas.create_line(*to_screen(*p1), *to_screen(*p2), fill=color)

def draw_path(points, color):
    return canvas.create_line([to_screen(x, y) for x, y in points], fill=color)

def trace(source, vel):
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

        for x0, y0, x1, y1 in boxes:
            if x >= x0 and x <= x1 and y >= y0 and y <= y1:
                if min(x - x0, x1 - x) < min(y - y0, y1 - y):
                    if x - x0 < x1 - x:
                        vx = -abs(vx)
                        x = x0
                    else:
                        vx = +abs(vx)
                        x = x1
                else:
                    if y - y0 < y1 - y:
                        vy = -abs(vy)
                        y = y0
                    else:
                        vy = +abs(vy)
                        y = y1

        tgt_dist = math.dist(target, (x, y))
        min_tgt_dist = min(min_tgt_dist, tgt_dist)
        if tgt_dist < target_radius:
            return True, 0, travel, hist

        if math.dist(hist[-1], (x, y)) >= 0.5:
            hist.append((x, y))

    return False, min_tgt_dist - target_radius, travel, hist


boxes = [ # xmin, ymin, xmax, ymax
    [30, 20, 50, 25],
    [50, 20, 55, 40]
]

target = (40.0, 30.0)
target_radius = 2.0
source = (0.0, 0.0)

for x0, y0, x1, y1 in boxes:
    canvas.create_rectangle(*to_screen(x0, y0), *to_screen(x1, y1), outline='cyan', fill='blue')

draw_circle(*target, target_radius, 'red', 'white')
draw_line((source[0] - 2.0, source[1]), (source[0] + 2.0, source[1]), 'white')
draw_line((source[0], source[1] - 2.0), (source[0], source[1] + 2.0), 'white')

def random_2d_arr(dim1, dim2):
    return [[random.random() for _ in range(dim2)] for _ in range(dim1)]

def distort_2d_arr(arr, amplitude):
    for sub_arr in arr:
        for i in range(len(sub_arr)):
            sub_arr[i] += 2.0 * (random.random() - 0.5) * amplitude


def activation(x:float):
    K = 3
    return K * x / (1.0 + K * abs(x))

# hit, min_dist, travel, traj = trace(source, (15.0, 26.5))
# draw_path(traj, 'red' if hit else 'white')

nn = nn.Net()
traj_hist = []
gen_index = 0
MAX_GENS = 300

def tick():
    global nn, traj_hist, gen_index

    if gen_index < MAX_GENS:
        canvas.after(50, tick)

    nn.draw_weights(canvas, WIDTH, HEIGHT)

    best_try = None
    best_fun = 0.0
    best_traj, best_out = None, None
    for i in range(20):
        distortion = 0.1 if i >= 10 else 1.0 # todo: make smaller disortions when we are closer to our target
        nn2 = nn.make_distorted_copy(distortion)
        out2 = nn2.calc_forward(target)
        hit, min_dist, travel, traj = trace(source, out2)

        target_fun = min_dist + travel * 0.1
        if best_try is None or target_fun < best_fun:
            best_try = nn2
            best_fun = target_fun
            best_traj = traj
            best_out = out2

    print(f'Gen {gen_index}: target_fun {best_fun:.2f}, out: {best_out}')
    traj_hist.append(draw_path(best_traj, 'gray'))
    if len(traj_hist) > 30:
        canvas.delete(traj_hist[0])
        traj_hist = traj_hist[1:]

    nn = best_try
    gen_index += 1

canvas.after(200, tick)

root.mainloop()
