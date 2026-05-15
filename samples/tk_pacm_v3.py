import tkinter as tk
import math
import random

# размеры поля для рисования в пикселях
W = 3000
H = 2000

# инициализация TKinter, тут можно ничего не менять
root = tk.Tk()
canvas = tk.Canvas(root, width=W, height=H, bg='white')
canvas.pack(side="top", fill="both", expand=True)

size = 100
speed = 20

rails = {
    "AB":((100, 100), (500, 100), [], [("BE", 1), ("BC", 1)]),
    "BC":((500, 100), (500, 500), [("AB", -1), ("BE", 1)], []),
    "BE":((500, 100), (900, 100), [("BC", 1)], [("ED", 1)]),
    "ED":((900, 100), (900, 500), [("BE", -1)], [])
    }

class Obj:
    def __init__(self, isPlayer:bool, visual):
        self.isPlayer = isPlayer
        self.current_rail = "AB"
        self.pos = 0.0
        self.direction = 0 if isPlayer else 1
        self.visual = visual
        canvas.moveto(self.visual, *self.get_lefttop())

    def get_lefttop(self):
        rail = rails[self.current_rail]
        p1, p2, _, _ = rail
        l = math.dist(p1, p2)
        t = self.pos / l
        x = p1[0] * (1.0 - t) + t * p2[0]
        y = p1[1] * (1.0 - t) + t * p2[1]
        return x - (size // 2), y - (size // 2)
    

    def move_key(self, dx, dy):
        pass
    

    def tick(self):
        rail = rails[self.current_rail]
        p1, p2, links1, links2 = rail
        
        l = math.dist(p1, p2)

        self.pos += speed * self.direction

        canvas.moveto(self.visual, *self.get_lefttop())

        if self.direction == 1 and self.pos >= l:
            self.pos = l
            if not self.isPlayer:
                self.switch_rail(links2)
        if self.direction == -1 and self.pos <= 0.0:
            self.pos = 0.0
            if not self.isPlayer:
                self.switch_rail(links1)


    def switch_rail(self, links):
        if len(links) == 0:
            self.direction = -1 if self.direction == 1 else 1
            return
        new_rail, new_dir = random.choice(links)
        self.current_rail = new_rail
        self.direction = new_dir
        np1, np2, _, _ = rails[new_rail]
        self.pos = 0.0 if new_dir == 1 else math.dist(np1, np2)



for name, rail in rails.items():
    p1, p2, links1, links2 = rail
    canvas.create_line(*p1, *p2, fill="blue")
    canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, fill="red", text=name)


objects = [Obj(True, canvas.create_arc(0, 0, size, size, fill="yellow", start=45, extent=270))]

for i in range(2):
    clr = random.choice(['red', 'blue', 'magenta'])
    objects.append(Obj(False, canvas.create_arc(0, 0, size, size, fill=clr, start=45, extent=180)))

# обработка события "нажата кнопка"
def on_key(event):
    global horizontal, vertical

    if event.keysym == 'w':
        vertical = -1 

    if event.keysym == 's':
        vertical = 1
        
    if event.keysym == 'a':
        horizontal = -1

    if event.keysym == 'd':
        horizontal = 1

def tick():
    global x, y, size, direction, current_rail, pos, objects
    canvas.after(50, tick)

    for o in objects:
        o.tick()


# регистрируем событие "кнопка"
root.bind('<Key>', on_key)

canvas.after(50, tick)


# необходимый оператор, без него окно сразу закроется!
root.mainloop()
