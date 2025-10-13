"""
SID: 25098892g
NAME: LUO DONGPU

The player operation timer class.
"""

import pygame
from comp import *
import time


class Timer(GraphicComponent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.font = pygame.font.Font("font/04B_0.TTF", 8)
        self.font_large = pygame.font.Font("font/04B_0.TTF", 15)
        self.pre_text = self.font.render(f"The dinosaur was active for", False, ctx.timer_text_color)
        self.pre_text_rect = self.pre_text.get_rect()
        self.pre_text_rect.center = \
            round(ctx.win.resolution[0] * ctx.timer_text_offset_x_per), ctx.win.resolution[1] // 2
        self.round_start_time = 0
        self.round_last_time = 0

    def update(self):
        self.round_last_time = time.time() - self.round_start_time

    def render(self):
        self.ctx.win.display.blit(self.pre_text, self.pre_text_rect)
        text = self.font_large.render(f"{self.round_last_time: .2f}", True, (50, 50, 50))
        rect = text.get_rect()
        rect.midleft = self.pre_text_rect.midright
        self.ctx.win.display.blit(text, rect)

    def restart_round(self):
        self.round_start_time = time.time()
