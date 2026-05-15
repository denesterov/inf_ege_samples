import tkinter as tk
import math
import random

# размеры поля для рисования в пикселях
W = 1200
H = 850

# инициализация TKinter, тут можно ничего не менять
root = tk.Tk()
canvas = tk.Canvas(root, width=W, height=H, bg='white')
canvas.pack(side='top', fill='both', expand=True)

size = 100
speed = 10
tick_dur = 40

s_nodes = {
    'BL': (100, 700),
    'TL': (100, 100),
    'TR': (1100, 100),
    'BR': (1100, 700),
    'TC': (600, 100),
    'BC': (600, 700),

    'M1C': (600, 300),
    'M1L': (100, 300),
    'M1R': (1100, 300),
    'M1RR': (950, 300),

    'M2CC': (450, 500),
    'M2C': (600, 500),
    'M2L': (100, 500),
    'M2R': (1100, 500),
}

s_edges = [
    ('TL', 'TC'),
    ('TC', 'TR'),
    ('TC', 'M1C'),
    ('BC', 'BL'),
    ('BC', 'BR'),

    ('TL', 'M1L'),
    ('M1L', 'M1C'),
    ('M1R', 'TR'),
    ('M1C', 'M1RR'),

    ('M2L', 'BL'),
    ('M2C', 'BC'),
    ('M2R', 'BR'),
    ('M2L', 'M2CC'),
    ('M2R', 'M2C'),

    ('M1L', 'M2L'),
    ('M1R', 'M2R'),
    ('M1C', 'M2C'),
]


def get_nodes(edge_idx:int):
    n1, n2 = s_edges[edge_idx]
    return s_nodes[n1], s_nodes[n2]


def get_links(node_id):
    inc = [(idx, +1) for idx, (n1, _) in enumerate(s_edges) if n1 == node_id]
    out = [(idx, -1) for idx, (_, n2) in enumerate(s_edges) if n2 == node_id]
    return inc + out


class Obj:
    def __init__(self, isPlayer:bool, visual):
        self.isPlayer = isPlayer
        self.current_edge = 0
        self.pos = 0.0
        self.direction = 0 if isPlayer else 1
        self.visual = visual
        canvas.moveto(self.visual, *self.get_lefttop())

    def get_lefttop(self):
        p1, p2 = get_nodes(self.current_edge)
        l = math.dist(p1, p2)
        t = self.pos / l
        x = p1[0] * (1.0 - t) + t * p2[0]
        y = p1[1] * (1.0 - t) + t * p2[1]
        return x - (size // 2), y - (size // 2)
    

    def move_key(self, dx, dy):
        if dx < 0: # tmp
            self.direction = -1
        if dx > 0: # tmp
            self.direction = +1
    

    def tick(self):
        n1, n2 = s_edges[self.current_edge]
        p1, p2 = s_nodes[n1], s_nodes[n2]
        
        l = math.dist(p1, p2)

        self.pos += speed * self.direction

        canvas.moveto(self.visual, *self.get_lefttop())

        if self.direction == 1 and self.pos >= l:
            self.pos = l
            if not self.isPlayer:
                self.switch_rail(n2)
        if self.direction == -1 and self.pos <= 0.0:
            self.pos = 0.0
            if not self.isPlayer:
                self.switch_rail(n1)


    def switch_rail(self, node_id):
        links = get_links(node_id)
        if len(links) == 0:
            self.direction = 0 if self.isPlayer else -self.direction
            return
        new_edge, new_dir = random.choice(links)
        self.current_edge = new_edge
        self.direction = new_dir
        p1, p2 = get_nodes(new_edge)
        self.pos = 0.0 if new_dir == 1 else math.dist(p1, p2)



def debug_draw():
    for idx, (n1, n2) in enumerate(s_edges):
        p1, p2 = s_nodes[n1], s_nodes[n2]
        canvas.create_line(*p1, *p2, fill='blue')
        canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, fill='red', text=f'{n1}-{n2}({idx})')
    for name, (x, y) in s_nodes.items():
        canvas.create_text(x, y, fill='red', text=name)
debug_draw()


objects = [Obj(True, canvas.create_arc(0, 0, size, size, fill='yellow', start=45, extent=270))]

for i in range(2):
    clr = random.choice(['red', 'blue', 'magenta'])
    objects.append(Obj(False, canvas.create_arc(0, 0, size, size, fill=clr, start=-15, extent=210)))


# обработка события "нажата кнопка"
def on_key(event):
    if event.keysym == 'a':
        objects[0].move_key(-1, 0)

    if event.keysym == 'd':
        objects[0].move_key(+1, 0)

def tick():
    canvas.after(tick_dur, tick)

    for o in objects:
        o.tick()


# регистрируем событие "кнопка"
root.bind('<Key>', on_key)

canvas.after(tick_dur, tick)


# необходимый оператор, без него окно сразу закроется!
root.mainloop()
