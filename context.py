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
        self.clear_color = Color(255, 255, 255, 255)
        self.UI_color = Color(20, 20, 20, 255)

        # dino
        self.dino_suspend_time = 3.0
        self.dino_suspend_init_spd = 360
        self.dino_suspend_spd = 280
        self.dino_suspend_de_acc_duration = 0.4
        self.dino_rot_duration = 0.12
        self.dino_anim_duration = 0.1
        self.dino_col_rect_scale_per = (0.3, 0.3)
        self.suspend_bar_color1 = Color("#95e1d3")
        self.suspend_bar_color2 = Color("#f38181")

        # ground
        self.ground_edge_px = 9
        self.ground_move_speed = 0.5

        # timer
        self.timer_text_offset_x_per = 0.4
        self.timer_text_color = Color(100, 100, 100)

        # manager
        self.cactus_types = 6
        self.gen_interval_range = (0.08, .5)#(0.02, .5)
        self.gen_interval_inv_hit_range = (0.02, 0.1)
        self.gen_speed_range = (150.0, 230.0)#(80.0, 160.0)
        self.difficulty_step_sec = 10
        self.difficulty_step_duration = 1  # ori 1.0
        self.difficulty_step_bar_width_per = 0.02
        self.difficulty_step_bar_interval_width_per = 0.013

        # invincible mode
        self.invincible_last_time_sec = 5.0
        self.cactus_invincible_speed_mul = 4.0
        self.cactus_invincible_speed_up_duration = 2.2
        self.cactus_inv_hit_speed = 300#550.0
        self.cactus_inv_hit_rot_vel = 1500.0
        self.invincible_bar_color1 = Color("#fcbad3")
        self.invincible_bar_color2 = Color("#a8d8ea")
        self.end_inv_shine_duration = 1.6

    def handle_event(self, event):
        if event.key == pygame.K_d:
            self.debug_rect = not self.debug_rect

    def close(self):
        # self.tkp.quit()
        pass
