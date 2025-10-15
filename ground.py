"""
SID: 25098892g
NAME: LUO DONGPU

Ground class.
"""
import pygame_shaders
from context import Context
from comp import *
from pygame_shaders import Shader
import pygame


class Ground(GraphicComponent):
    def __init__(self, ctx):
        super().__init__(ctx)
        ctx.ground = self
        self.sprite = pygame.image.load("imgs/ground.png")
        self.rect = self.sprite.get_rect()

        self.rect_top = pygame.Rect(self.rect)
        self.rect_top.width = ctx.win.resolution[0]
        self.rect_top.topleft = (0, 0)

        self.rect_bottom = pygame.Rect(self.rect_top)
        self.rect_bottom.bottomleft = (0, ctx.win.resolution[1])

        self.rect_left = pygame.Rect(self.rect_top)
        self.rect_left.size = self.rect_left.size[1], self.rect_left.size[0]
        self.rect_left.topleft = (0, 0)

        self.rect_right = pygame.Rect(self.rect_left)
        self.rect_left.topright = (ctx.win.resolution[0], 0)

        self.ground_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "shaders/ground.glsl", self.sprite)
        self.ground_shader.send("speed", ctx.ground_move_speed)
        # self.ground_shader.send("resolution", self.sprite.get_rect().size)

    def set_inv_move_speed(self, is_invincible: bool):
        self.ground_shader.send("speed",
                                self.ctx.ground_inv_move_speed if is_invincible else self.ctx.ground_move_speed)

    def update(self):
        self.ground_shader.send("time", self.ctx.win.app_time)

    def render(self):
        grd = self.ground_shader.render()
        self.ctx.win.display.blit(grd, self.rect_bottom)

        grd2 = pygame.transform.rotate(grd, 180)
        self.ctx.win.display.blit(grd2, self.rect_top)

        grd3 = pygame.transform.rotate(grd, 90)
        self.ctx.win.display.blit(grd3, self.rect_left)

        grd4 = pygame.transform.rotate(grd, -90)
        self.ctx.win.display.blit(grd4, self.rect_right)
