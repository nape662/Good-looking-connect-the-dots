from dots import *
from button import *

FPS = 60
WAIT_FOR_LINE = pg.event.custom_type()
WAIT_FOR_DOUBLECLICK = pg.event.custom_type()
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 800
BG_COLOR = (240, 228, 202, 255)
PAUSE_BUTTON_X = SCREEN_WIDTH * 0.25
PAUSE_BUTTON_Y_RELATIVE = 0.33
PAUSE_BUTTON_WIDTH = SCREEN_WIDTH * 0.5
PAUSE_TRANSITION_LENGTH = 25


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
        self.background_highlight_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_highlight_surface.set_alpha(0)
        self.game_tick = 0
        self.transition_tick = 0
        self.running = False
        self.FPS = FPS
        self.follow_mouse = False
        self.recently_clicked = False
        self.recently_popped = list()
        self.connected = list()
        self.lines = list()  # each item in lines is a set containing 2 Dots
        self.dots = [[0] * 6 for i in range(6)]
        for i in range(6):
            for j in range(5, -1, -1):
                self.dots[i][j] = Dot(i, j, self)
        self.buttons = list()
        self.continue_button = Button(self, (PAUSE_BUTTON_X, SCREEN_HEIGHT * PAUSE_BUTTON_Y_RELATIVE),
                                      "Unpause", PAUSE_BUTTON_WIDTH, COLOUR_LIST[2])
        self.restart_button = Button(self,
                                     (PAUSE_BUTTON_X, SCREEN_HEIGHT * PAUSE_BUTTON_Y_RELATIVE + SCREEN_WIDTH * 0.15),
                                     "Restart", PAUSE_BUTTON_WIDTH, COLOUR_LIST[3])
        self.buttons.append(self.restart_button)
        self.buttons.append(self.continue_button)
        self.mode = None
        self.restart()
        # self.mode set in Dots.fly() when dots flew in/out properly

    def pause(self):
        self.mode = "Pause transition"
        self.transition_tick = 1
        self.handle_connected()
        for i in self.dots:
            for j in i:
                j.fly_out()
        for i in self.buttons:
            i.fly_in()

    def unpause(self):
        self.mode = "Pause transition"
        self.transition_tick = PAUSE_TRANSITION_LENGTH + 1
        for i in self.dots:
            for j in i:
                j.fly_in()
        for i in self.buttons:
            i.fly_out()

    def restart(self):
        self.mode = "Pause transition"
        self.transition_tick = PAUSE_TRANSITION_LENGTH + 1
        for i in self.buttons:
            i.fly_out()
        self.game_tick = 1
        for i in range(6):
            for j in range(5, -1, -1):
                self.dots[i][j] = Dot(i, j, self)

    def draw_line(self, new_dot):
        self.connected.append(new_dot)
        new_dot.current_highlight_frame = 1
        if self.just_made_loop():
            for i in range(6):
                for j in range(6):
                    if self.dots[i][j].colour_number == self.connected[0].colour_number:
                        self.dots[i][j].current_highlight_frame = 1
        self.lines.append({self.connected[-1], self.connected[-2]})
        self.set_follow_mouse_timer()
        self.recently_clicked = False

    def shorten_line(self):
        self.connected.pop(-1)
        self.lines.pop(-1)
        self.set_follow_mouse_timer()

    def line_follow_mouse(self):
        if self.follow_mouse and self.connected and (
                self.connected[-1].current_falling_frame == 0 or self.connected[-1].current_falling_frame >= 7):
            pg.draw.line(self.screen, self.connected[-1].colour, self.connected[-1].rect.center, pg.mouse.get_pos(),
                         width=10)

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

    def just_made_loop(self):
        for i in self.connected[:-1]:
            if i == self.connected[-1]:
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
                        self.dots[dotx][doty].current_highlight_frame = 1
                    elif self.dots[dotx][doty].colour_number == self.connected[-1].colour_number and (
                            (dotx == self.connected[-1].column and abs(doty - self.connected[-1].row) == 1) or (
                            doty == self.connected[-1].row and abs(dotx - self.connected[-1].column) == 1)):
                        if self.lines and {self.connected[-1], self.dots[dotx][doty]} == self.lines[-1]:
                            self.shorten_line()
                        elif {self.connected[-1], self.dots[dotx][doty]} not in self.lines:
                            self.draw_line(self.dots[dotx][doty])
        except AttributeError:  # if click on screen then release off-screen, you get AttributeError
            pass

    def handle_inputs(self):
        if self.mode == "Game" and self.game_tick >= 10:
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
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause()
            if pg.mouse.get_pressed()[0]:
                self.handle_mouse()
        elif self.mode == "Pause":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.continue_button.mouse_in_button():
                        self.unpause()
                    if self.restart_button.mouse_in_button():
                        self.restart()

    def exclude_impossible(self):  # checks if there are dots to pair up
        for i in range(6):
            for j in range(5):
                if self.dots[i][j].colour_number == self.dots[i][j + 1].colour_number \
                        or self.dots[j][i].colour_number == self.dots[j + 1][i].colour_number:
                    return False
        for i in range(6):
            for j in range(6):
                self.dots[i][j].pop()

    def draw_on_screen(self):
        self.screen.fill(BG_COLOR)
        if self.mode == "Game" and self.game_tick >= 10:
            for i in self.recently_popped:
                i.disappear()
            for i in self.dots:
                for j in i:
                    j.update_position()
                    j.highlight()
            for i in self.lines:
                first_dot, second_dot = i
                pg.draw.line(self.screen, first_dot.colour, first_dot.rect.center, second_dot.rect.center,
                             width=10)
            self.line_follow_mouse()
            if self.connected_has_loop():
                self.background_highlight_surface.set_alpha(40)
                self.background_highlight_surface.fill(self.connected[0].colour)
            else:
                self.background_highlight_surface.set_alpha(0)
            self.screen.blit(self.background_highlight_surface, (0, 0))
        elif self.mode == "Pause transition":
            self.continue_button.fly()
            self.restart_button.fly()
            for i in self.dots:
                for j in i:
                    j.fly()
        elif self.mode == "Pause":
            self.continue_button.draw()
            self.restart_button.draw()
        pg.display.flip()

    def run(self):
        self.running = True
        while self.running:
            pg.time.Clock().tick_busy_loop(FPS)
            self.handle_inputs()
            self.exclude_impossible()
            self.draw_on_screen()
            if self.mode == "Game":
                self.game_tick += 1
            elif self.mode == "Pause transition":
                self.transition_tick += 1
                if self.transition_tick == PAUSE_TRANSITION_LENGTH:
                    self.mode = "Pause"
                elif self.transition_tick == 2 * PAUSE_TRANSITION_LENGTH:
                    self.mode = "Game"
        return 0


def main():
    x = App()
    x.run()


main()
