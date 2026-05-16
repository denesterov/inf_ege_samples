import tkinter as tk
import math
import random

import tk_pacm_v3_map as map

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


class Obj:
    def __init__(self, isPlayer:bool, visual):
        self.isPlayer = isPlayer
        self.current_edge = 0
        self.pos = 0.0
        self.direction = 0 if isPlayer else 1
        self.visual = visual
        canvas.moveto(self.visual, *self.get_lefttop())

    def get_lefttop(self):
        p1, p2, _, _ = map.get_nodes(self.current_edge)
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
        p1, p2, n1, n2 = map.get_nodes(self.current_edge)
        
        l = math.dist(p1, p2)

        self.pos += speed * self.direction
        self.pos = max(0, min(self.pos, l))

        canvas.moveto(self.visual, *self.get_lefttop())

        if self.direction == 1 and self.pos >= l:
            self.switch_rail(n2)
        if self.direction == -1 and self.pos <= 0.0:
            self.switch_rail(n1)


    def switch_rail(self, node_id):
        links = map.get_links(node_id)
        if len(links) == 0:
            self.direction = 0 if self.isPlayer else -self.direction
            return
        new_edge, new_dir = random.choice(links)
        self.current_edge = new_edge
        self.direction = 0 if self.isPlayer else new_dir
        p1, p2, _, _ = map.get_nodes(new_edge)
        self.pos = 0.0 if new_dir == 1 else math.dist(p1, p2)


map.debug_draw(canvas)

objects = [Obj(True, canvas.create_arc(0, 0, size, size, fill='yellow', start=45, extent=270))]

for i in range(3):
    clr = ['red', 'blue', 'green', 'cyan'][i % 3]
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


root.bind('<Key>', on_key)
canvas.after(tick_dur, tick)


root.mainloop()
