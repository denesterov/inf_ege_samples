import tkinter as tk
import copy
import math
import random


def random_2d_arr(dim1, dim2):
    return [[random.random() for _ in range(dim2)] for _ in range(dim1)]


def distort_2d_arr(arr, amplitude):
    for sub_arr in arr:
        for i in range(len(sub_arr)):
            sub_arr[i] += 2.0 * (random.random() - 0.5) * amplitude


def activation(x:float):
    K = 3
    return K * x / (1.0 + K * abs(x))


def lerp_rgb_color(r0, g0, b0, r1, g1, b1, s):
    return f'#{int(r0 * (1.0-s) + r1 * s):02x}{int(g0 * (1.0-s) + g1 * s):02x}{int(b0 * (1.0-s) + b1 * s):02x}'

class Net:
    INPUT = 2
    LAYER1 = 10
    LAYER2 = 6
    OUTPUT = 2


    def __init__(self):
        # state
        self.linksA = random_2d_arr(self.LAYER1, self.INPUT)
        self.linksB = random_2d_arr(self.LAYER2, self.LAYER1)
        self.linksC = random_2d_arr(self.OUTPUT, self.LAYER2)

        # saved from last calc
        self.input = [0.0] * self.INPUT
        self.layer1 = [0.0] * self.LAYER1
        self.layer2 = [0.0] * self.LAYER2
        self.output = [0.0] * self.OUTPUT

        self.weights_visuals = []


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


    def make_distorted_copy(self, ampl):
        obj = copy.deepcopy(self)

        distort_2d_arr(obj.linksA, ampl)
        distort_2d_arr(obj.linksB, ampl)
        distort_2d_arr(obj.linksC, ampl)

        return obj


    def draw_weights(self, canvas, width, height):
        for o in self.weights_visuals: canvas.delete(o)
        self.weights_visuals = []
        self._draw_weight_bars(canvas, width)
        self._draw_weight_links(canvas, width, 330)


    def _draw_weight_bars(self, canvas, width):
        x_start = width - 150
        y_start = 30
        row_h = 22
        bar_h = 10
        bar_w = 2
        bar_sp = 2
        row_i = 0
        x_offs = x_start
        for wei in [self.linksA, self.linksB, self.linksC]:
            for ww in wei:
                for wi, w in enumerate(ww):
                    wa = activation(w)
                    bar_delta = bar_w + bar_sp
                    x0 = x_offs + wi * bar_delta
                    x1 = x0 + bar_w
                    y0 = y_start + row_h * row_i + row_h
                    y1 = y0 - int(bar_h * wa)
                    clr_t = min(abs(w) / 10.0, 1.0)
                    color = lerp_rgb_color(64, 255, 255, 255, 64, 64, clr_t) if w >= 0 else lerp_rgb_color(64, 64, 255, 255, 255, 64, clr_t)
                    id = canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
                    self.weights_visuals.append(id)

                if len(ww) > 4 or ww == wei[-1]:
                    row_i += 1
                    x_offs = x_start
                else:
                    x_offs += (1 + len(ww)) * (bar_w + bar_sp)
            row_i += 1

    def _draw_weight_links(self, canvas:tk.Canvas, width:int, start_y:int):
        y_spacing = 80
        graph_width = 330
        x_left = width - 30 - graph_width

        y = start_y

        for wei in [self.linksA, self.linksB, self.linksC]:
            # wei is [outputs x inputs]
            outp_num = len(wei)
            inp_num = len(wei[0])
            for outp_idx, inp_w in enumerate(wei):
                for inp_idx, w in enumerate(inp_w):
                    x0 = x_left + (inp_idx + 1) * graph_width // (inp_num + 1)
                    x1 = x_left + (outp_idx + 1) * graph_width // (outp_num + 1)

                    clr_t = min(abs(w) / 10.0, 1.0)
                    color = lerp_rgb_color(0, 64, 64, 0, 255, 255, clr_t) if w >= 0 else lerp_rgb_color(64, 0, 0, 255, 0, 0, clr_t)
                    id = canvas.create_line(x0, y, x1, y + y_spacing, fill=color,width=2)
                    self.weights_visuals.append(id)
            y += y_spacing
