from dots import *


# фишка класса это что если у тебя происходит все внутри одного объекта,
# то его поля по факту глобальные и (self.x ~= global x)


def get_square_coord(coords):
    x, y = coords
    dotx = max(min(int((x - (SCREEN_WIDTH - 600) / 2) // 100), 5), 0)
    doty = max(min(int((y - 175) // 100), 5), 0)  # might change if we change window size
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

    def draw_line(self, new_dot):
        pg.draw.line(self.screen, self.connected[-1].colour, self.connected[-1].rect.center, new_dot.rect.center,
                     width=10)
        self.connected.append(new_dot)

    def shorten_line(self):
        pg.draw.line(self.screen, BG_COLOR, self.connected[-1].rect.center, self.connected[-2].rect.center, width=10)
        self.connected.pop(-1)

    def handle_connected(self):
        self.screen.fill(BG_COLOR)  # erases all lines
        if len(self.connected) > 1:
            if self.connected_has_loop():
                loop_colour_number = self.connected[0].colour_number
                for i in range(6):  # use in range to control order of popping dots
                    for j in range(6):
                        if self.dots[i][j].colour_number == loop_colour_number:
                            self.dots[i][j].pop(in_loop=True)
            else:
                for i in self.connected:
                    i.pop()
        self.connected.clear()

    def connected_has_loop(self):
        for i in range(len(self.connected)):
            for j in range(i):
                if self.connected[i] == self.connected[j]:
                    return True
        return False

    def grid_has_pairs(self):
        for i in range(6):
            for j in range(5):
                if self.dots[i][j].colour_number == self.dots[i][j+1] or self.dots[j][i] == self.dots[j+1][i]:
                    return False
        return True

    def handle_mouse(self, event):
        try:
            dotx, doty = get_square_coord(event.pos)

            if not self.connected:
                self.connected.append(self.dots[dotx][doty])
            elif self.dots[dotx][doty] != self.connected[-1] and self.dots[dotx][doty].colour_number == self.connected[-1].colour_number:
                if (dotx == self.connected[-1].column and abs(doty - self.connected[-1].row) <= 1) or (
                        doty == self.connected[-1].row and abs(dotx - self.connected[-1].column <= 1)):
                    if len(self.connected) > 1 and self.dots[dotx][doty] == self.connected[-2]:
                        self.shorten_line()
                    elif self.connected_has_loop() and self.dots[dotx][doty] in self.connected:
                        pass
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
                elif event.type == pg.KEYDOWN:  # cheat for testing
                    dotx, doty = get_square_coord(pg.mouse.get_pos())
                    self.dots[dotx][doty].pop()

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
