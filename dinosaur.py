"""
SID: 25098892g
NAME: LUO DONGPU

The dinosaur (player) character.
"""

from typing import Callable
import pygame
from comp import *
from tween import Tween, Ease
from utils import *
import time


class Dino(GraphicComponent):
    """
    The Dinosaur (player) character class
    """
    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.ctx.dino = self

        self.v = self.ctx.dino_suspend_spd
        self.vx: Callable = self.__get_zero_speed
        self.vy: Callable = self.__get_suspend_speed
        self.cur_rot: float = 0.0
        self.tar_rot: float = 0.0
        self.is_update_suspend = True
        self.dir: int = 0

        # animation
        self.run_frames = [
            pygame.image.load("imgs/dino/dino1.png").convert_alpha(),
            pygame.image.load("imgs/dino/dino2.png").convert_alpha()
        ]
        self.bend_frames = [
            pygame.image.load("imgs/dino/dino_bend1.png").convert_alpha(),
            pygame.image.load("imgs/dino/dino_bend2.png").convert_alpha()
        ]
        self.hit_frame = pygame.image.load("imgs/dino/dino_hit.png").convert_alpha()
        self.sprite = self.run_frames[0]
        self.next_frame_time: float = 0
        self.sprite_idx = 0

        self.rect = self.sprite.get_rect()
        self.rect.center = self.ctx.win.resolution[0]//2, self.ctx.win.resolution[1]//2
        self.col_rect = pygame.Rect(self.rect)
        self.col_rect.size = round(self.rect.size[0]*self.ctx.dino_col_rect_scale_per[0])\
            , round(self.rect.size[1]*self.ctx.dino_col_rect_scale_per[1])

        self.rot_tween = Tween()
        self.suspend_de_acc_tween = Tween()

        self.update()  # init state

    def handle_event(self, event: Event):
        rot: int = 0
        change_dir = False
        if event.key == pygame.K_UP:
            if self.dir == 3:
                return
            self.dir = 3
            self.vx = self.__get_zero_speed
            self.vy = self.__get_negative_suspend_speed
            rot = 180
            self.is_update_suspend = True
            change_dir = True
        elif event.key == pygame.K_DOWN:
            if self.dir == 0:
                return
            self.dir = 0
            self.vx = self.__get_zero_speed
            self.vy = self.__get_suspend_speed
            rot = 0
            self.is_update_suspend = True
            change_dir = True
        elif event.key == pygame.K_LEFT:
            if self.dir == 2:
                return
            self.dir = 2
            self.vx = self.__get_negative_suspend_speed
            self.vy = self.__get_zero_speed
            rot = 270
            self.is_update_suspend = True
            change_dir = True
        elif event.key == pygame.K_RIGHT:
            if self.dir == 1:
                return
            self.dir = 1
            self.vx = self.__get_suspend_speed
            self.vy = self.__get_zero_speed
            rot = 90
            self.is_update_suspend = True
            change_dir = True
        else:
            return

        if change_dir:
            self.suspend_de_acc_tween.to_float(self.ctx.dino_suspend_init_spd, self.ctx.dino_suspend_spd,
                                               self.ctx.dino_suspend_de_acc_duration,
                                               self.__set_suspend_spd, ease=Ease.OutCubic)

        if rot != self.cur_rot:
            self.cur_rot, self.tar_rot = shortest_arc(self.cur_rot, rot)
            # print(self.cur_rot, self.tar_rot)
            duration = 0.001+self.ctx.dino_rot_duration * abs(self.tar_rot - self.cur_rot) / 90
            self.rot_tween.to_float(self.cur_rot, self.tar_rot, duration,
                                    self.__set_rot, ease=Ease.OutQuad)

    def __get_suspend_speed(self) -> float:
        return self.v

    def __get_negative_suspend_speed(self) -> float:
        return -self.v

    @staticmethod
    def __get_zero_speed() -> float:
        return 0.0

    def __set_rot(self, rot: float):
        self.cur_rot = rot

    def __set_suspend_spd(self, spd: float):
        self.v = spd

    def update(self):
        # update position
        if self.is_update_suspend:
            pts = self.ctx.win.delta_time
            self.rect.move_ip(pts * self.vx(), pts * self.vy())

            ep = self.ctx.ground_edge_px
            wh = self.ctx.win.resolution

            if self.rect.left < ep:
                self.rect.left = ep
                self.__ground()
            if self.rect.right > wh[0]-ep:
                self.rect.right = wh[0]-ep
                self.__ground()
            if self.rect.top < ep:
                self.rect.top = ep
                self.__ground()
            if self.rect.bottom > wh[1]-ep:
                self.rect.bottom = wh[1]-ep
                self.__ground()

            self.col_rect.center = self.rect.center

        # update animation
        if time.time() > self.next_frame_time:
            frames = self.bend_frames if self.is_update_suspend else self.run_frames
            self.next_frame_time = time.time() + self.ctx.dino_anim_duration
            self.sprite_idx = (self.sprite_idx + 1) % len(frames)

    def __ground(self):
        self.vx = 0
        self.vy = 0
        self.is_update_suspend = False

    def render(self):
        frames = self.bend_frames if self.is_update_suspend else self.run_frames
        self.sprite = pygame.transform.rotate(frames[self.sprite_idx], self.cur_rot)
        self.ctx.win.display.blit(self.sprite, self.rect)

        if self.ctx.debug_rect:
            pygame.draw.rect(self.ctx.win.display, (255, 0, 0), self.col_rect, width=1)
