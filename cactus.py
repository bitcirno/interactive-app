"""
SID: 25098892g
NAME: LUO DONGPU

Cactus obstacle class.
"""

import pygame
from comp import GraphicComponent


class Cactus(GraphicComponent):
    def __init__(self, ctx, sprite, rect, vx, vy):
        super().__init__(ctx)
        self.is_active = True
        self.sprite = sprite
        self.rect = rect
        self.vx = vx
        self.vy = vy

    def update(self):
        if not self.is_active:
            return
        pts = self.ctx.win.delta_time
        self.rect.x = round(self.rect.x + pts * self.vx)
        self.rect.y = round(self.rect.y + pts * self.vy)
        if self.rect.colliderect(self.ctx.dino.col_rect):
            print("hit")
        if not self.rect.colliderect(self.ctx.win.px_rect):  # out screen
            self.is_active = False

    def render(self):
        if not self.is_active:
            return
        self.ctx.win.display.blit(self.sprite, self.rect)
