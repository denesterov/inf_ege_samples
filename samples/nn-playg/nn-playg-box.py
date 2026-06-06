
class Box:
    def __init__(self, xx0, yy0, xx1, yy1):
        self.x0 = xx0
        self.y0 = yy0
        self.x1 = xx1
        self.y1 = yy1

    def point_collide(self, x, y, vx, vy):
        if x >= self.x0 and x <= self.x1 and y >= self.y0 and y <= self.y1:
            if min(x - self.x0, self.x1 - x) < min(y - self.y0, self.y1 - y):
                if x - self.x0 < self.x1 - x:
                    vx = -abs(vx)
                    x = self.x0
                else:
                    vx = +abs(vx)
                    x = self.x1
            else:
                if y - self.y0 < self.y1 - y:
                    vy = -abs(vy)
                    y = self.y0
                else:
                    vy = +abs(vy)
                    y = self.y1
            return True, x, y, vx, vy

        return False, x, y, vx, vy

    def draw(self, canvas, to_screen):
        return canvas.create_rectangle(*to_screen(self.x0, self.y0), *to_screen(self.x1, self.y1), outline='cyan', fill='blue')
