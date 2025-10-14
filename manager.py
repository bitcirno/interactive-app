"""
SID: 25098892g
NAME: LUO DONGPU

Game manager module controlling the game rules and flow
"""

import time
import pygame
from utils import *
import random
from cactus import Cactus
from comp import *
from tween import Tween, Ease


class Manager(object):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.ctx.mgr = self
        self.next_gen_time = 0

        self.cactus_imgs = [pygame.image.load(f"imgs/cactus/cactus{i}.png")
                            for i in range(1, ctx.cactus_types + 1)]
        self.active_cactus = []

        # invincible mode
        self.invincible_mode = False
        self.invincible_timer = Tween()
        self.cactus_speed_mul = 1.0
        self.cactus_speed_up_tween = Tween()
        self.end_inv_shine = False
        self.end_inv_shine_img = pygame.Surface(self.ctx.win.resolution,
                                                flags=pygame.SRCALPHA).convert_alpha()
        self.end_inv_shine_img.fill("white")
        self.end_inv_shine_tween = Tween()

    def bind_timer_events(self, timer):
        timer.on_increase_dif_level_step = self.__enter_invincible
        timer.on_suspend_timeout = self.__suspend_timeout

    def __suspend_timeout(self):
        print("suspend timeout")
        exit(-1)

    def __enter_invincible(self):
        self.ctx.timer.stop_suspend_timer()  # stop suspend timer if entering invincible mode
        self.invincible_mode = True
        self.invincible_timer.to_float(1.0, 0.0, self.ctx.invincible_last_time_sec,
                                       self.ctx.timer.update_invincible_bar, self.__exit_invincible,
                                       ease=Ease.Linear)
        self.cactus_speed_up_tween.to_float(1.0, self.ctx.cactus_invincible_speed_mul,
                                            self.ctx.cactus_invincible_speed_up_duration,
                                            self.__set_cactus_speed_mul, ease=Ease.OutQuad)
        self.__increase_difficulty()

    def __set_cactus_speed_mul(self, mul: float):
        self.cactus_speed_mul = mul

    def __exit_invincible(self):
        self.invincible_mode = False
        self.cactus_speed_mul = 1.0
        self.ctx.timer.restart_dif_step_timer()
        if self.ctx.dino.is_update_suspend:  # start suspend timer if dino is still in air
            self.ctx.timer.restart_suspend_timer()

        # shine effect, while removing all cactus
        self.end_inv_shine = True
        self.end_inv_shine_tween.to_float(1.0, 0.0, self.ctx.end_inv_shine_duration,
                                          self.__set_end_inv_shine_alpha, self.__end_end_inv_shine,
                                          ease=Ease.OutQuad)
        self.active_cactus.clear()

    def __set_end_inv_shine_alpha(self, a: float):
        self.end_inv_shine_img.set_alpha(round(a * 255))

    def __end_end_inv_shine(self):
        self.end_inv_shine_img.fill("white")

    def __increase_difficulty(self):
        ...

    def update(self):
        # remove inactive cactus (out of screen)
        for i in range(len(self.active_cactus) - 1, -1, -1):
            if not self.active_cactus[i].is_active:
                self.active_cactus.pop(i)

        if time.time() > self.next_gen_time:
            rge = self.ctx.gen_interval_inv_hit_range if self.invincible_mode else self.ctx.gen_interval_range
            interval = get_random_float_between(*rge)
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
                rect.bottomleft = reso[0], reso[1] - edge
                vx = -speed
            elif track == 1:  # right
                img = pygame.transform.rotate(img, 90)
                rect.size = rect.height, rect.width
                rect.bottomright = reso[0] - edge, 0
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

    def render_top_shine(self):
        if not self.end_inv_shine:
            return
        self.ctx.win.display.blit(self.end_inv_shine_img, (0, 0))

