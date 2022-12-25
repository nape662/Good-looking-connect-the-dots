from dots import *

# фишка класса это что если у тебя происходит все внутри одного объекта,
# то его поля по факту глобальные и (self.x means global x)


def get_square_coord(coords):
    x, y = coords
    dotx = int((x - (SCREEN_WIDTH - 600) / 2) // 100)
    doty = int((y - 175) // 100)
    if dotx > 5:
        dotx = 5
    if doty > 5:
        doty = 5
    if dotx < 0:
        dotx = 0
    if doty < 0:
        dotx = 0
    return dotx, doty


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.screen.fill(BG_COLOR)
        self.running = False

        self.dots = [[0] * 6 for i in range(6)]
        for i in range(6):
            for j in range(6):
                self.dots[j][i] = (Dot(j, i, self.screen, self.dots))
        self.connected = list()
        self.lines = list()

    def draw_line(self, new_dot):
        pg.draw.line(self.screen, self.connected[-1].colour, self.connected[-1].rect.center, new_dot.rect.center, width=10)
        self.connected.append(new_dot)

    def shorten_line(self):
        pg.draw.line(self.screen, BG_COLOR, self.connected[-1].rect.center, self.connected[-2].rect.center, width=10)
        self.connected.pop(-1)

    def handle_connected(self):
        self.screen.fill(BG_COLOR)  # erases all lines
        if len(self.connected) > 1:
            for i in self.connected:
                i.pop()
        self.connected.clear()

    def handle_mouse(self, event):
        try:
            dotx, doty = get_square_coord(event.pos)

            if not self.connected:
                self.connected.append(self.dots[dotx][doty])
            elif self.dots[dotx][doty] != self.connected[-1] and self.dots[dotx][doty].colour == self.connected[
                -1].colour:
                if (dotx == self.connected[-1].column and abs(doty - self.connected[-1].row) <= 1) or (
                        doty == self.connected[-1].row and abs(dotx - self.connected[-1].column <= 1)):
                    if len(self.connected) > 1 and self.dots[dotx][doty] == self.connected[-2]:
                        self.shorten_line()
                    else:
                        self.draw_line(self.dots[dotx][doty])
        except AttributeError:  # if click on screen release off screen get AttributeError
            pass

    def run(self):
        # main loop
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif pg.mouse.get_pressed()[0]:
                    self.handle_mouse(event)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.handle_connected()

            # draws to screen
            for i in self.dots:
                for j in i:
                    self.screen.blit(j.surface, j.rect)
            pg.display.flip()
        return 0


def main():
    x = App()
    x.run()


main()
