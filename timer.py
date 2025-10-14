"""
SID: 25098892g
NAME: LUO DONGPU

The player operation timer class.
"""
from typing import Callable

import pygame
from pygame.color import Color
from comp import *
import time
from tween import Tween, Ease


class Timer(GraphicComponent):
    def __init__(self, ctx):
        super().__init__(ctx)
        ctx.timer = self

        # round timer
        self.font = pygame.font.Font("font/04B_0.TTF", 8)
        self.font_large = pygame.font.Font("font/04B_0.TTF", 15)
        self.pre_text = self.font.render(f"Meters that Dino runs", False, ctx.timer_text_color)
        self.pre_text_rect = self.pre_text.get_rect()
        self.pre_text_rect.center = \
            round(ctx.win.resolution[0] * ctx.timer_text_offset_x_per), ctx.win.resolution[1] // 2
        self.round_start_time = 0
        self.round_last_time = 0

        # difficulty step bar
        self.dif_step: int = 0
        self.next_dif_step_time: int = 0
        self.dif_bar_width = ctx.win.resolution[0] * ctx.difficulty_step_bar_width_per
        self.dif_bar_interval_width = ctx.win.resolution[0] * ctx.difficulty_step_bar_interval_width_per
        total_width = (self.dif_bar_width*ctx.difficulty_step_sec
                       + (ctx.difficulty_step_sec-1)*self.dif_bar_interval_width)
        self.dif_step_bar = pygame.Surface((total_width, self.dif_bar_width),
                                           flags=pygame.SRCALPHA).convert_alpha()
        self.dif_step_bar_rect = self.dif_step_bar.get_rect()
        self.dif_step_bar_rect.topright = self.pre_text_rect.bottomright
        self.__render_difficult_step_bar()

        # event functions
        self.on_increase_dif_level_step: Callable | None = None
        self.on_suspend_timeout: Callable | None = None

        # background timer bar
        self.suspend_timer_tween = Tween()
        self.suspend_bar_rect = pygame.Rect(0, 0, *self.ctx.win.resolution)
        self.suspend_bar_color: Color = Color("white")
        self.invincible_bar_rect = pygame.Rect(0, 0, *self.ctx.win.resolution)
        self.invincible_bar_color: Color = Color("white")

    def update_invincible_bar(self, per: float):  # 1 -> 0
        self.invincible_bar_rect.height = self.ctx.win.resolution[1] * per
        self.invincible_bar_color = self.ctx.invincible_bar_color2.lerp(self.ctx.invincible_bar_color1, per)

    def __update_suspend_bar(self, per: float):  # 1 -> 0
        self.suspend_bar_rect.height = self.ctx.win.resolution[1] * per
        self.suspend_bar_color = self.ctx.suspend_bar_color2.lerp(self.ctx.suspend_bar_color1, per)

    def __render_difficult_step_bar(self):
        self.dif_step_bar.fill(self.ctx.clear_color)
        rect_x = 0
        for i in range(self.ctx.difficulty_step_sec):
            width = 0 if i < self.dif_step else 1
            pygame.draw.rect(self.dif_step_bar, self.ctx.UI_color,
                             (rect_x, 0, self.dif_bar_width, self.dif_bar_width), width)
            rect_x += self.dif_bar_width + self.dif_bar_interval_width
        # pygame.image.save(self.dif_step_bar, "dif_step_bar.png")

    def update(self):
        self.round_last_time = time.time() - self.round_start_time
        if not self.ctx.mgr.invincible_mode and self.round_last_time > self.next_dif_step_time:
            self.next_dif_step_time = self.round_last_time + self.ctx.difficulty_step_duration
            self.dif_step += 1
            self.__render_difficult_step_bar()
            if self.dif_step == self.ctx.difficulty_step_sec:
                self.on_increase_dif_level_step()  # increase level step by 1
                self.dif_step = 0

    def render(self):
        # render invincible bar
        if self.ctx.mgr.invincible_mode:
            pygame.draw.rect(self.ctx.win.display, self.invincible_bar_color, self.invincible_bar_rect, 0)
        elif self.ctx.dino.is_update_suspend:
            pygame.draw.rect(self.ctx.win.display, self.suspend_bar_color, self.suspend_bar_rect, 0)

        # render meter text
        self.ctx.win.display.blit(self.pre_text, self.pre_text_rect)
        text = self.font_large.render(f"{self.round_last_time: .2f}", True, self.ctx.UI_color)
        rect = text.get_rect()
        rect.midleft = self.pre_text_rect.midright
        self.ctx.win.display.blit(text, rect)
        self.ctx.win.display.blit(self.dif_step_bar, self.dif_step_bar_rect)

    def restart_dif_step_timer(self):
        self.dif_step = 0
        self.next_dif_step_time = self.round_last_time + self.ctx.difficulty_step_duration
        self.__render_difficult_step_bar()

    def restart_suspend_timer(self):
        self.suspend_timer_tween.to_float(1.0, 0.0, self.ctx.dino_suspend_time,
                                          self.__update_suspend_bar, self.on_suspend_timeout,
                                          Ease.Linear)

    def stop_suspend_timer(self):
        self.suspend_timer_tween.kill()

    def restart_round(self):
        self.dif_step = 0
        self.round_start_time = time.time()
        self.round_last_time = 0
        self.next_dif_step_time = self.round_last_time + self.ctx.difficulty_step_duration
        self.__render_difficult_step_bar()
