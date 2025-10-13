"""
SID: 25098892g
NAME: LUO DONGPU

Game context, managing game components and parameters
"""


import pygame.font
from pygame.color import Color
from win import PixelGameWindow


class Context:
    def __init__(self):
        self.win: PixelGameWindow = None
        self.timer = None
        self.mgr = None
        self.ground = None
        self.dino = None
        # self.tkp = tkparam.TKParamWindow()

        self.debug_rect = True

        # dino
        self.dino_suspend_init_spd = 500
        self.dino_suspend_spd = 330
        self.dino_suspend_de_acc_duration = 0.4
        self.dino_rot_duration = 0.2
        self.dino_anim_duration = 0.12
        self.dino_col_rect_scale_per = (0.45, 0.45)

        # ground
        self.ground_edge_px = 9
        self.ground_move_speed = 0.5

        # timer
        self.timer_text_offset_x_per = 0.4
        self.timer_text_color = Color(100, 100, 100)

    def close(self):
        # self.tkp.quit()
        pass
