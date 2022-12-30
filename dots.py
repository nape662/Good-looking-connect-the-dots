from random import randint, choice
import pygame as pg

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 800
BG_COLOR = (240, 228, 202, 255)
COLOUR_LIST = [(125, 179, 73), (210, 106, 70), (243, 192, 58), (123, 85, 125), (90, 191, 211)]


def row_into_y(y):
    return (y + 1.75) * 100


class Dot:
    def __init__(self, column, row, app, exclude_this_colour=None):
        self.app = app
        self.row = row
        self.column = column
        self.x = self.column * 100 + (SCREEN_WIDTH - 600) / 2
        self.y = row_into_y(self.row) - 400

        # if you make a loop then dots of this colour shouldn't spawn after you clear the loop
        if exclude_this_colour is not None:
            numbers = [i for i in range(len(COLOUR_LIST))]
            numbers.pop(exclude_this_colour)
            self.colour_number = choice(numbers)
            self.colour = COLOUR_LIST[self.colour_number]
        else:
            self.colour_number = randint(0, len(COLOUR_LIST) - 1)
            self.colour = COLOUR_LIST[self.colour_number]

        # drawing to screen
        self.surface = pg.Surface((100, 100))
        self.surface.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect = self.surface.get_rect(left=self.x, top=self.y)
        pg.draw.circle(self.surface, self.colour, center=(50, 50), radius=25)

        # other animation stuff
        self.current_falling_frame = 1
        self.current_disappearing_frame = 0

    def drop(self):
        # immediately becomes lower dot as a game element
        if self.row < 5:
            self.app.dots[self.column][self.row + 1] = self
        self.row += 1
        if self.current_falling_frame <= 12:
            self.current_falling_frame = max(1, min(self.current_falling_frame, 7))  # min-max for chained falls
        else:
            self.current_falling_frame = 1  # for future wobbling

    def pop(self, in_loop=False):
        self.app.recently_popped.append(self)
        self.current_disappearing_frame = 1
        for i in range(self.row-1, -1, -1):
            self.app.dots[self.column][i].drop()
        if in_loop:
            self.app.dots[self.column][0] = Dot(self.column, 0, self.app, self.colour_number)
        else:
            self.app.dots[self.column][0] = Dot(self.column, 0, self.app)

    def movement_coefficient(self):
        return (row_into_y(self.row) - self.y) / (169 - self.current_falling_frame**2)  # this is to aid with wobbling and

    def fall(self):
        # there are 12 frames when it falls
        if 1 <= self.current_falling_frame <= 12:
            self.y += (2 * self.current_falling_frame + 1) * self.movement_coefficient()
            self.rect = self.surface.get_rect(left=self.x, top=self.y)
            self.current_falling_frame += 1
        # then it should wobble in elifs for next 12 frames (just copy frame by frame what's happening in original game)
        # elif 12 < self.current_falling_frame <= 24:
        #    self.y += ((self.current_falling_frame % 2) - 0.5) * 10
        #    self.rect = self.surface.get_rect(left=self.x, top=self.y)
        #    self.current_falling_frame += 1
        elif self.current_falling_frame > 12:
            self.y = round(self.y)
            self.rect = self.surface.get_rect(left=self.x, top=self.y)
            self.current_falling_frame = 0

    def disappear(self):
        if 6 >= self.current_disappearing_frame >= 1:
            self.surface.fill((0, 0, 0))  # it's transparent
            pg.draw.circle(self.surface, self.colour, center=(50, 50), radius=25-(self.current_disappearing_frame * 4))
            self.current_disappearing_frame += 1
        elif self.current_disappearing_frame > 6:
            for i in self.app.recently_popped:
                if i == self:
                    self.app.recently_popped.remove(self)

    def highlight(self):
        pass

