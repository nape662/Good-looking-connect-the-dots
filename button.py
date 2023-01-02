import pygame as pg


class Button:
    def __init__(self, app, position, text, width, colour, command=lambda: print("No command activated for this button")):
        self.app = app
        self.x, self.y = position
        self.x += 600
        self.width = width
        self.height = width * 0.2
        self.surface = pg.Surface((width, width*0.2))
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect(left=self.x, top=self.y, width=self.width, height=self.height)
        pg.draw.rect(self.surface, colour, (0, 0, self.width, self.height), border_radius=int(self.height * 0.5))
        self.font = pg.font.Font(None, 64)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center = (self.width * 0.5, self.height * 0.5), width=self.width-20, height=self.height-20)
        self.command = command
        self.current_flying_frame = 0

    def mouse_in_button(self):
        x, y = pg.mouse.get_pos()
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        else:
            return False

    def draw(self):
        self.app.screen.blit(self.surface, self.rect)
        self.surface.blit(self.text, self.text_rect)

    def fly_in(self):
        if self.current_flying_frame == 0:
            self.current_flying_frame = 1

    def fly_out(self):
        if self.current_flying_frame == 7:
            self.current_flying_frame = 8

    def fly(self):
        if 1 <= self.current_flying_frame <= 6:
            self.x -= 100
        elif 13 >= self.current_flying_frame >= 8:
            self.x += 100
        elif self.current_flying_frame > 13:
            self.current_flying_frame = 0
        self.rect = self.surface.get_rect(left=self.x, top=self.y)
        self.text_rect = self.text.get_rect(center=(self.width * 0.5, self.height * 0.5))
        if self.current_flying_frame != 0 and self.current_flying_frame != 7:
            self.current_flying_frame += 1
        self.draw()

