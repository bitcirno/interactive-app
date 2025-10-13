import pygame
from random import randint


class Cube(object):
    def __init__(self, s):
        self.s = s
        self.edge = 6
        self.rect = pygame.rect.Rect(s.width / 2, s.height / 2, self.edge, self.edge)
        self.v = 280
        self.vx = 0
        self.vy = self.v
        self.cube_color = (24, 116, 205)
        self.suspend = False

        self.bar_color1 = [154, 205, 50]
        self.bar_color2 = [255, 99, 71]
        self.rounded_bar_color = [0, 0, 0]
        self.bar_color = self.bar_color1.copy()
        self.decrease_time = 210.0
        self.color_decrease_value = [(self.bar_color1[i] - self.bar_color2[i]) / self.decrease_time for i in range(3)]
        self.bar_rect = pygame.rect.Rect(0, 0, self.s.width, self.s.height)
        self.bar_height = self.s.height
        self.bar_decrease_value = self.s.width / self.decrease_time

    def decrease_suspension_time(self):
        self.decrease_time -= 10
        self.color_decrease_value = [(self.bar_color1[i] - self.bar_color2[i]) / self.decrease_time for i in range(3)]
        self.bar_decrease_value = self.s.width / self.decrease_time

    def update(self, pts):
        self.rect.x = round(self.rect.x + pts * self.vx)
        self.rect.y = round(self.rect.y + pts * self.vy)
        if self.rect.left < self.s.cube_range[0]:
            self.rect.left = self.s.cube_range[0]
            self.__freeze()
        if self.rect.right > self.s.cube_range[1]:
            self.rect.right = self.s.cube_range[1]
            self.__freeze()
        if self.rect.top < self.s.cube_range[0]:
            self.rect.top = self.s.cube_range[0]
            self.__freeze()
        if self.rect.bottom > self.s.cube_range[1]:
            self.rect.bottom = self.s.cube_range[1]
            self.__freeze()
        if self.suspend:
            self.__bar_decrease()

    def display(self):
        pygame.draw.rect(self.s.screen, self.cube_color, self.rect, 0)

    def to_up(self):
        self.vy = -self.v
        self.vx = 0
        self.suspend = True

    def to_down(self):
        self.vy = self.v
        self.vx = 0
        self.suspend = True

    def to_left(self):
        self.vx = -self.v
        self.vy = 0
        self.suspend = True

    def to_right(self):
        self.vx = self.v
        self.vy = 0
        self.suspend = True

    def __freeze(self):
        self.vx = 0
        self.vy = 0
        self.suspend = False
        self.__bar_reset()

    def reset(self):
        self.rect.x = self.s.width / 2
        self.rect.y = self.s.height / 2
        self.vx = 0
        self.vy = self.v
        self.__bar_reset()
        self.decrease_time = 220.0

    def __bar_reset(self):
        self.bar_rect = pygame.rect.Rect(0, 0, self.s.width, self.s.height)
        self.bar_height = self.s.height
        self.bar_color = self.bar_color1.copy()
        self.suspend = False

    def __bar_decrease(self):
        self.bar_height -= self.bar_decrease_value
        if self.bar_height <= 0:
            self.s.game_over = True
            pygame.time.set_timer(self.s.COUNT, 0)
            self.bar_height = 0
        self.bar_rect.height = round(self.bar_height)
        for i in range(3):
            self.bar_color[i] -= self.color_decrease_value[i]
            self.rounded_bar_color[i] = round(self.bar_color[i])
            if self.rounded_bar_color[i] > 255:
                self.rounded_bar_color[i] = 255
            elif self.rounded_bar_color[i] < 0:
                self.rounded_bar_color[i] = 0

    def bar_display(self):
        pygame.draw.rect(self.s.screen, self.rounded_bar_color, self.bar_rect)

