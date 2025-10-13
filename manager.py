"""
SID: 25098892g
NAME: LUO DONGPU

Game manager module controlling the game rules and flow
"""

import time
import pygame
from utils import *
import random
from context import Context
from cactus import Cactus
from comp import *


class Manager(object):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.ctx.mgr = self
        self.next_gen_time = 0

        self.cactus_imgs = [pygame.image.load(f"imgs/cactus/cactus{i}.png")
                            for i in range(1, ctx.cactus_types+1)]
        self.active_cactus = []

    def update(self):
        # remove inactive cactus (out of screen)
        for i in range(len(self.active_cactus)-1, -1, -1):
            if not self.active_cactus[i].is_active:
                self.active_cactus.pop(i)

        if time.time() > self.next_gen_time:
            interval = get_random_float_between(*self.ctx.gen_interval_range)
            self.next_gen_time = time.time() + interval

            img = random.choice(self.cactus_imgs)
            if random.random() < 0.5:
                img = pygame.transform.flip(img, True, False)  # random flip

            rect = img.get_rect()
            track = random.randint(0, 3)
            reso = self.ctx.win.resolution
            edge = self.ctx.ground_edge_px
            speed = get_random_float_between(*self.ctx.gen_speed_range)
            vx = 0
            vy = 0

            if track == 0:  # bottom
                rect.bottomleft = reso[0], reso[1]-edge
                vx = -speed
            elif track == 1:  # right
                img = pygame.transform.rotate(img, 90)
                rect.size = rect.height, rect.width
                rect.bottomright = reso[0]-edge, 0
                vy = speed
            elif track == 2:  # top
                img = pygame.transform.flip(img, False, True)
                rect.topright = 0, edge
                vx = speed
            else:  # left
                img = pygame.transform.rotate(img, -90)
                rect.size = rect.height, rect.width
                rect.topleft = edge, reso[1]
                vy = -speed

            cactus = Cactus(self.ctx, img, rect, vx, vy)
            self.active_cactus.append(cactus)

        for cactus in self.active_cactus:
            cactus.update()

    def render_cactus(self):
        # print(len(self.active_cactus))
        for cactus in self.active_cactus:
            cactus.render()
