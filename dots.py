from random import randint, choice
import pygame as pg

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 800
BG_COLOR = (240, 228, 202, 255)
COLOUR_LIST = [(125, 179, 73), (210, 106, 70), (243, 192, 58), (123, 85, 125), (90, 191, 211)]


def row_into_y(row):
    return (row + 1.75) * 100


class Dot:
    def __init__(self, column, row, app, exclude_this_colour=None):
        self.app = app
        self.row = row
        self.column = column
        self.x = self.column * 100 + (SCREEN_WIDTH - 600) / 2
        self.y = row_into_y(self.row) - SCREEN_HEIGHT

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
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect(left=self.x, top=self.y)
        pg.draw.circle(self.surface, self.colour, center=(50, 50), radius=25)

        # other animation stuff
        if self.row == 0:
            if self.app.dots[self.column][1].current_falling_frame < 0:
                self.current_falling_frame = self.app.dots[self.column][1].current_falling_frame - 4
            else:
                self.current_falling_frame = -11
        else:
            self.current_falling_frame = -7 + (self.row-5) * 4
        self.coefficient = self.movement_coefficient()
        self.current_disappearing_frame = 0
        self.current_highlight_frame = 0
        self.highlight_surface = pg.Surface((100, 100))
        self.highlight_surface.set_colorkey((0, 0, 0))
        self.current_flying_frame = 0

    # Setzt die Wartezeit vor dem Fall
    def drop(self):
        if self.row < 5:
            self.app.dots[self.column][self.row + 1] = self
        self.row += 1
        self.coefficient = self.movement_coefficient()
        if self.coefficient < 4:  # thing doesn't fall from the very top
            delay = 4 * round(self.coefficient * 1.68)  # because movement_coefficient() basically counts row difference
        else:
            delay = 4 * self.row
        if self.row < 5:
            if self.app.dots[self.column][self.row+1].current_falling_frame == 0:
                self.current_falling_frame = -3 - delay
            else:  # can't be above 0 with current algorithm
                self.current_falling_frame = self.app.dots[self.column][self.row+1].current_falling_frame - 4
        else:
            self.current_falling_frame = -3 - delay

    # Fall-Animation, ist jeder Tick ausführt, nicht jeder Tick bewegt sich aber der Dot
    def update_position(self):
        # there are 12 frames when it falls
        if self.current_falling_frame < 0:
            self.current_falling_frame += 2
        elif 1 <= self.current_falling_frame <= 12:
            self.y += (2 * self.current_falling_frame + 1) * self.coefficient
            self.rect = self.surface.get_rect(left=self.x, top=self.y)
            self.current_falling_frame += 1
        # then it should wobble in elif's for next 12 frames (just copy frame by frame what's happening in original game)
        elif 13 <= self.current_falling_frame <= 16:  # to speed up some falls when dots have just landed (still need to wobble here)
            self.y = round(self.y)
            self.rect = self.surface.get_rect(left=self.x, top=self.y)
            self.current_falling_frame += 1
        elif self.current_falling_frame > 16:
            self.current_falling_frame = 0
        self.app.screen.blit(self.surface, self.rect)

    # Hilfe für update_position
    def movement_coefficient(self):
        return (row_into_y(self.row) - self.y) / 168  # this is to aid with wobbling and chained falls

    # Beginnt Verschwinden (ruft drop() von anderen) und schafft einen neuen Dot
    def pop(self, in_loop=False, continue_game=True):
        self.app.recently_popped.append(self)
        self.current_disappearing_frame = 1
        for i in range(self.row - 1, -1, -1):
            self.app.dots[self.column][i].drop()
        if continue_game:
            if in_loop:
                self.app.dots[self.column][0] = Dot(self.column, 0, self.app, self.colour_number)
            else:
                self.app.dots[self.column][0] = Dot(self.column, 0, self.app)

    # Animation von Verschwinden
    def disappear(self):
        if 6 >= self.current_disappearing_frame >= 1:
            self.surface.fill((0, 0, 0))
            pg.draw.circle(self.surface, self.colour, center=(50, 50), radius=25-(self.current_disappearing_frame * 4))
            self.current_disappearing_frame += 1
            self.app.screen.blit(self.surface, self.rect)
        elif self.current_disappearing_frame > 6:
            self.app.recently_popped.remove(self)

    # Animation von Highlight
    def highlight(self):
        if 0 < self.current_highlight_frame <= 3:
            self.current_highlight_frame += 1
        elif 4 <= self.current_highlight_frame <= 24:
            self.highlight_surface.fill((0, 0, 0))
            self.highlight_surface.set_alpha(255 - self.current_highlight_frame * 10)
            pg.draw.circle(self.highlight_surface, self.colour, center=(50, 50), radius=25+self.current_highlight_frame)
            self.current_highlight_frame += 1
            self.app.screen.blit(self.highlight_surface, self.rect)
        elif self.current_highlight_frame > 20:
            self.highlight_surface.set_alpha(0)
            self.current_highlight_frame = 0

    # 3 letzte für Transition Mode
    def fly(self):
        if 2 <= self.current_flying_frame <= 7:
            self.x -= 125
        elif 9 <= self.current_flying_frame <= 15:
            self.x += 125
        elif self.current_flying_frame == 16 or self.current_flying_frame == 17 or self.current_flying_frame == 24:
            self.x -= 10
        elif 18 <= self.current_flying_frame <= 23:
            self.x -= 15
        elif self.current_flying_frame == 25:
            self.x -= 5
            self.current_flying_frame = 0
            pg.draw.circle(self.surface, self.colour, center=(50, 50), radius=25)
        if self.current_flying_frame != 0 and self.current_flying_frame != 8:
            self.current_flying_frame += 1
        self.rect = self.surface.get_rect(left=self.x, top=self.y)
        self.app.screen.blit(self.surface, self.rect)

    def fly_out(self):
        self.y = row_into_y(self.row)
        self.rect = self.surface.get_rect(left=self.x, top=self.y)
        self.current_falling_frame = 0
        self.current_highlight_frame = 0
        self.current_flying_frame = 1
        pg.draw.circle(self.surface, (255, 255, 255), center=(50, 50), radius=25)

    def fly_in(self):
        self.current_flying_frame = 9
