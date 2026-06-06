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


class Net:
    INPUT = 2
    LAYER1 = 10
    LAYER2 = 6
    OUTPUT = 2

    weights_visuals = []


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

        xc = width - 70
        y_start = 50
        row_h = 22
        bar_h = 10
        bar_w = 10
        bar_sp = 5
        row_i = 0
        for wei in [self.linksA, self.linksB, self.linksC]:
            for ww in wei:
                row_i += 1
                for wi, w in enumerate(ww):
                    w = activation(w)
                    bar_delta = bar_w + bar_sp
                    x0 = xc - len(wei[0]) * bar_delta // 2 + wi * bar_delta
                    x1 = x0 + bar_w
                    y0 = y_start + row_h * row_i
                    y1 = y0 - int(bar_h * w)
                    id = canvas.create_rectangle(x0, y0, x1, y1, fill='cyan' if w >= 0 else 'blue')
                    self.weights_visuals.append(id)
