import tkinter as tk
import math
import random

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
    canvas.create_line([to_screen(x, y) for x, y in points], fill=color)

def trace(source, vel):
    x, y = source[0], source[1]
    ax, ay = 0.0, -9.81
    vx, vy = vel
    t = 0.0
    dt = 0.1
    hist = [(x, y)]
    min_tgt_dist = math.dist((x, y), target)
    while y >= 0.0 and t < 10.0:
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

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
            return True, 0, hist

        if math.dist(hist[-1], (x, y)) >= 0.5:
            hist.append((x, y))

    return False, min_tgt_dist, hist


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

def random_arr(dim1, dim2):
    return [[random.random() for _ in range(dim2)] for _ in range(dim1)]

def activation(x:float):
    K = 3
    return K * x / (1.0 + K * abs(x))

class Net:
    INPUT = 2
    LAYER1 = 10
    LAYER2 = 6
    OUTPUT = 2

    def __init__(self):
        # state
        self.linksA = random_arr(self.LAYER1, self.INPUT)
        self.linksB = random_arr(self.LAYER2, self.LAYER1)
        self.linksC = random_arr(self.OUTPUT, self.LAYER2)

        # saved from last calc
        self.input = [0.0] * self.INPUT
        self.layer1 = [0.0] * self.LAYER1
        self.layer2 = [0.0] * self.LAYER2
        self.output = [0.0] * self.OUTPUT


    def calc_forward(self, inp: list[float]):
        assert len(inp) == self.INPUT
        self.input[:] = inp
        self.layer1[:] = [0.0] * self.LAYER1
        self.layer2[:] = [0.0] * self.LAYER2
        self.output[:] = [0.0] * self.OUTPUT

        self.layer1[:] = [activation(sum(input * weight for input, weight in zip(self.input, links))) for links in self.linksA]

        self.layer2[:] = [activation(sum(L1 * weight for L1, weight in zip(self.layer1, links))) for links in self.linksB]

        self.output[:] = [sum(L2 * weight for L2, weight in zip(self.layer2, links)) for links in self.linksC]

        return self.output


hit, min_dist, hist = trace(source, (15.0, 27.5))

draw_path(hist, 'red' if hit else 'white')

nn = Net()
out = nn.calc_forward([10.0, 20.0])
print(out)

root.mainloop()
