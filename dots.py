from random import choice
import pygame as pg

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 800
BG_COLOR = (240, 228, 202, 255)
COLOUR_LIST = [(125, 179, 73), (210, 106, 70), (243, 192, 58), (123, 85, 125), (90, 191, 211)]

# inherit Sprite class with no real purpose tbh (in class Dot)
# since I'm not using collision or group draw methods


class Dot(pg.sprite.Sprite):
    def __init__(self, column, row, screen, dots):
        pg.sprite.Sprite.__init__(self)

        self.dots = dots  # 2 dimensional list
        self.row = row
        self.column = column
        self.colour = choice(COLOUR_LIST)

        # drawing to screen
        self.screen = screen
        self.surface = pg.Surface((50, 50))
        self.surface.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect = self.surface.get_rect(left=(self.column * 100 + (SCREEN_WIDTH - 550) / 2), top=(self.row + 2) * 100)
        pg.draw.circle(self.surface, self.colour, center=(25, 25), radius=25)

        # self.is_falling = False  # animation later

    def drop(self):
        # self.is_falling = True
        if self.row < 5:
            self.dots[self.column][self.row + 1] = self
        self.row += 1

        self.rect = self.surface.get_rect(left=(self.column * 100 + (SCREEN_WIDTH - 550) / 2), top=(self.row + 2) * 100)
        pg.draw.circle(self.surface, self.colour, center=(25, 25), radius=25)

    def pop(self):
        self.surface.fill(BG_COLOR)
        for i in range(self.row-1, -1, -1):  # to maintain order of drop()
            self.dots[self.column][i].drop()
        self.dots[self.column][0] = Dot(self.column, 0, self.screen, self.dots)
        # self.screen.blit(self.surface, self.rect)
        # need to figure out: drop then another while animation
