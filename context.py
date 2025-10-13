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

        self.debug_rect = False

        # dino
        self.dino_suspend_init_spd = 360
        self.dino_suspend_spd = 280
        self.dino_suspend_de_acc_duration = 0.4
        self.dino_rot_duration = 0.2
        self.dino_anim_duration = 0.1
        self.dino_col_rect_scale_per = (0.3, 0.3)

        # ground
        self.ground_edge_px = 9
        self.ground_move_speed = 0.5

        # timer
        self.timer_text_offset_x_per = 0.4
        self.timer_text_color = Color(100, 100, 100)

        # manager
        self.cactus_types = 6
        self.gen_interval_range = (0.5, 1.0)
        # self.gen_interval_range = (0.05, 0.3)
        self.gen_speed_range = (80.0, 160.0)

    def handle_event(self, event):
        if event.key == pygame.K_d:
            self.debug_rect = not self.debug_rect

    def close(self):
        # self.tkp.quit()
        pass
