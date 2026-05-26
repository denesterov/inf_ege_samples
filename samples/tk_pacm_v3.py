import tkinter as tk
import math
import random
import tk_pacm_v3_map as map


W = 1200
H = 850

root = tk.Tk()
canvas = tk.Canvas(root, width=W, height=H, bg='white')
canvas.pack(side='top', fill='both', expand=True)

size = 100
speed = 10
tick_dur = 40

next_move = None

balls = {}

class Obj:
    def __init__(self, isPlayer:bool, isDead:bool, visual):
        self.isPlayer = isPlayer
        if isPlayer == True:
            self.current_edge = 3
        else:
            self.current_edge = 0
        self.pos = 0.0
        self.isDead = isDead
        self.direction = 0 if isPlayer else 1
        self.visual = visual
        canvas.moveto(self.visual, *self.get_lefttop())

    def get_lefttop(self):
        x, y = self.get_center()
        return x - (size // 2), y - (size // 2)

    def get_center(self):
        p1, p2 = map.get_nodes(self.current_edge)
        l = math.dist(p1, p2)
        t = self.pos / l
        x = p1[0] * (1.0 - t) + t * p2[0]
        y = p1[1] * (1.0 - t) + t * p2[1]
        return x, y

    def redraw_visual(self, p1, p2):
        x, y = self.get_lefttop()
        st = 0
        if p1[0] < p2[0]:
            st = 45
        if p1[0] > p2[0]:
            st = 225
        if p1[1] < p2[1]:
            st = 315
        if p1[1] > p2[1]:
            st = 135
        canvas.delete(self.visual)
        self.visual = canvas.create_arc(x, y, x + size, y + size, fill='yellow', start=st, extent=270)

    def move_key(self, dx, dy):
        if self.direction != 0:
            p1, p2 = map.get_nodes(self.current_edge, self.direction == -1)
            rx, ry = p2[0] - p1[0], p2[1] - p1[1]
            if dx * rx + dy * ry < 0:
                self.direction = -self.direction
                self.redraw_visual(p2, p1)
                return True
            return False

        if self.direction == 0:
            for edge_idx, dir in map.get_edge_links(self.current_edge, self.pos == 0.0):
                p1, p2 = map.get_nodes(edge_idx, dir == -1)
                l = math.dist(p1, p2)
                rx, ry = p2[0] - p1[0], p2[1] - p1[1]
                if dx * rx + dy * ry > 0.5 * l:
                    self.current_edge = edge_idx
                    self.direction = dir
                    self.pos = 0.0 if dir == 1 else l
                    self.redraw_visual(p1, p2)
                    return True
        return False


    def tick(self):
        p1, p2, n1, n2 = map.get_nodes_ex(self.current_edge)

        l = math.dist(p1, p2)

        self.pos += speed * self.direction
        self.pos = max(0, min(self.pos, l))

        canvas.moveto(self.visual, *self.get_lefttop())

        if self.direction == 1 and self.pos >= l:
            self.switch_rail(n2)
        if self.direction == -1 and self.pos <= 0.0:
            self.switch_rail(n1)

    def collide_with_balls(self):
        p = self.get_center()
        for ii, ball in balls.items():
            l = math.dist(ball, p)
            if l <= size // 3:
                del balls[ii]
                canvas.delete(ii)
                break

    def switch_rail(self, node_id):
        links = map.get_links(node_id, )
        if len(links) == 0:
            self.direction = 0 if self.isPlayer else -self.direction
            return
        new_edge, new_dir = random.choice(links)
        self.current_edge = new_edge
        self.direction = 0 if self.isPlayer else new_dir
        p1, p2 = map.get_nodes(new_edge)
        self.pos = 0.0 if new_dir == 1 else math.dist(p1, p2)


#map.debug_draw(canvas)

objects = [Obj(True, False, canvas.create_arc(0, 0, size, size, fill='yellow', start=45, extent=270))]

for i in range(3):
    clr = ['red', 'blue', 'green', 'cyan'][i % 3]
    objects.append(Obj(False, False, canvas.create_arc(0, 0, size, size, fill=clr, start=-15, extent=210)))

for n1, n2 in map.edges:
    p1, p2 = map.nodes[n1], map.nodes[n2]
    L = math.dist(p1, p2)
    dball = 100
    l = dball / 2
    r = 10
    while l < L:
        t = l/L
        x = p1[0]*(1-t) + p2[0] * t
        y = p1[1]*(1-t) + p2[1] * t
        ii = canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
        balls[ii] = (x, y)
        l += dball

def on_key(event):
    global next_move
    move_keys = {'a' : (-1, 0), 'd': (+1, 0), 'w': (0, -1), 's': (0, +1)}
    if event.keysym in move_keys:
        next_move = move_keys[event.keysym]


def tick():
    if objects[0].isDead == False:
        canvas.after(tick_dur, tick)

        objects[0].collide_with_balls()
    
        for o in objects:
            o.tick()

        for ghost in objects[1:]:
            c = ghost.get_center()
            pos = objects[0].get_center()
            if math.dist(c, pos) <= size // 3:
                canvas.create_text(W // 2, H // 2, fill="red", text="GAME OVER")
                objects[0].isDead = True

        global next_move
        if next_move is not None:
            if objects[0].move_key(*next_move):
                next_move = None


root.bind('<Key>', on_key)
canvas.after(tick_dur, tick)


root.mainloop()