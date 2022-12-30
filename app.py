from dots import *

FPS = 60
WAIT_FOR_LINE = pg.event.custom_type()
WAIT_FOR_DOUBLECLICK = pg.event.custom_type()
# Process finished with exit code -1073741819 (0xC0000005) ??????????????????


def get_square_coord(coords):
    x, y = coords
    return max(min(int((x - (SCREEN_WIDTH - 600) / 2) // 100), 5), 0), min(int((y - 175) // 100), 5)


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Dots")
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.screen.fill(BG_COLOR)
        self.running = False
        self.FPS = FPS
        self.follow_mouse = True
        self.recently_clicked = False
        self.recently_popped = list()
        self.connected = list()
        self.lines = list()  # each item in lines is a set containing 2 Dots
        self.dots = [[0] * 6 for i in range(6)]
        for i in range(6):
            for j in range(6):
                self.dots[i][j] = Dot(i, j, self)

    def draw_line(self, new_dot):
        self.connected.append(new_dot)
        new_dot.start_highlight()
        if self.connected_has_loop():
            for i in range(6):
                for j in range(6):
                    if self.dots[i][j].colour_number == self.connected[0].colour_number:
                        self.dots[i][j].start_highlight()
        self.lines.append({self.connected[-1], self.connected[-2]})
        self.set_follow_mouse_timer()
        self.recently_clicked = False

    def shorten_line(self):
        self.connected.pop(-1)
        self.lines.pop(-1)
        self.set_follow_mouse_timer()

    def line_follow_mouse(self):
        if self.follow_mouse and self.connected and (self.connected[-1].current_falling_frame == 0 or self.connected[-1].current_falling_frame >= 7):
            pg.draw.line(self.screen, self.connected[-1].colour, self.connected[-1].rect.center, pg.mouse.get_pos(), width=10)

    def set_follow_mouse_timer(self):
        pg.time.set_timer(WAIT_FOR_LINE, 100)
        self.follow_mouse = False

    def handle_doubleclick(self):
        if self.recently_clicked:
            dotx, doty = get_square_coord(pg.mouse.get_pos())
            if (dotx, doty) == self.recently_clicked:
                self.dots[dotx][doty].pop()
            pg.time.set_timer(WAIT_FOR_DOUBLECLICK, 0)
            self.set_follow_mouse_timer()
            self.recently_clicked = False
        else:
            self.recently_clicked = get_square_coord(pg.mouse.get_pos())
            pg.time.set_timer(WAIT_FOR_DOUBLECLICK, 400)

    def connected_has_loop(self):
        for i in range(len(self.connected)):
            for j in range(i):
                if self.connected[i] == self.connected[j]:
                    return True
        return False

    def handle_connected(self):
        if len(self.connected) > 1:
            if self.connected_has_loop():
                for i in range(6):
                    for j in range(6):
                        if self.dots[i][j].colour_number == self.connected[0].colour_number:
                            self.dots[i][j].pop(in_loop=True)
            else:
                for i in self.connected:
                    i.pop()
        self.connected.clear()
        self.lines.clear()

    def handle_mouse(self):
        try:
            dotx, doty = get_square_coord(pg.mouse.get_pos())
            if doty >= 0:
                if self.dots[dotx][doty].current_falling_frame == 0 or self.dots[dotx][doty].current_falling_frame >= 7:
                    if not self.connected:
                        self.connected.append(self.dots[dotx][doty])
                        self.dots[dotx][doty].start_highlight()
                    elif self.dots[dotx][doty].colour_number == self.connected[-1].colour_number and (
                            (dotx == self.connected[-1].column and abs(doty - self.connected[-1].row) == 1) or (
                                doty == self.connected[-1].row and abs(dotx - self.connected[-1].column) == 1)):
                        if self.lines and {self.connected[-1], self.dots[dotx][doty]} == self.lines[-1]:
                            self.shorten_line()
                        elif {self.connected[-1], self.dots[dotx][doty]} not in self.lines:
                            self.draw_line(self.dots[dotx][doty])
            else:
                self.follow_mouse = False  # so it doesn't follow when press way above the dots field
        except AttributeError:  # if click on screen then release off-screen, you get AttributeError
            pass

    def handle_inputs(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            elif event.type == pg.MOUSEBUTTONUP:
                self.handle_connected()
            elif event.type == WAIT_FOR_LINE:
                pg.time.set_timer(WAIT_FOR_LINE, 0)
                self.follow_mouse = True
            elif event.type == WAIT_FOR_DOUBLECLICK:
                pg.time.set_timer(WAIT_FOR_DOUBLECLICK, 0)
                self.recently_clicked = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_doubleclick()
        if pg.mouse.get_pressed()[0]:
            self.handle_mouse()

    def exclude_impossible(self):  # checks if there are dots to pair up
        for i in range(6):
            for j in range(5):
                if self.dots[i][j].colour_number == self.dots[i][j+1].colour_number\
                        or self.dots[j][i].colour_number == self.dots[j+1][i].colour_number:
                    return False
        for i in range(6):
            for j in range(6):
                self.dots[i][j].pop()

    def draw_on_screen(self):
        self.screen.fill(BG_COLOR)
        for i in self.recently_popped:
            i.disappear()
        for i in self.dots:
            for j in i:
                j.move()
                j.highlight()
        for i in self.lines:
            first_dot, second_dot = i
            pg.draw.line(self.screen, first_dot.colour, first_dot.rect.center, second_dot.rect.center,
                         width=10)
        self.line_follow_mouse()
        pg.display.flip()

    def run(self):
        self.running = True
        while self.running:
            pg.time.Clock().tick_busy_loop(FPS)
            self.handle_inputs()
            self.exclude_impossible()
            self.draw_on_screen()
        return 0


def main():
    x = App()
    x.run()


main()
