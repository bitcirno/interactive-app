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
        self.win: PixelGameWindow | None = None
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
        self.dino_suspend_inv_spd = 400
        self.dino_suspend_de_acc_duration = 0.4
        self.dino_rot_duration = 0.12
        self.dino_inv_rot_speed = -2600.0
        self.dino_anim_duration = 0.1
        self.dino_anim_inv_duration = 0.05
        self.dino_col_rect_scale_per = (0.3, 0.3)
        self.suspend_bar_color1 = Color("#95e1d3")
        self.suspend_bar_color2 = Color("#f38181")

        # ground
        self.ground_edge_px = 9
        self.ground_move_speed = 0.5
        self.ground_inv_move_speed = 1.8

        # timer
        self.timer_text_offset_x_per = 0.4
        self.timer_text_color = Color(100, 100, 100)
        self.meter_text_scale_large = 1.8
        self.meter_text_scale_upp_duration = 0.45

        # manager
        self.cactus_low_types = 6
        self.cactus_mid_types = 4
        self.cactus_tall_types = 3
        self.dif_level_add_mid_cactus = 2
        self.dif_level_add_tall_cactus = 4
        self.gen_interval_range = (0.5, 1.00)
        self.gen_interval_range_dif_step = 0.02
        self.gen_interval_inv_hit_range = (0.02, 0.08)
        self.gen_speed_range = (40.0, 80.0)
        self.gen_speed_range_max = (80.0, 110.0)
        self.gen_speed_range_dif_step = 8
        self.difficulty_step_sec = 9
        self.difficulty_step_duration = 1  # ori 1.0
        self.difficulty_step_bar_width_per = 0.02
        self.difficulty_step_bar_interval_width_per = 0.013

        # invincible mode
        self.invincible_last_time_sec = 4.0
        self.cactus_invincible_speed_mul = 5.0
        self.cactus_invincible_speed_up_duration = 2.2
        self.cactus_inv_hit_speed = 550.0
        self.cactus_inv_hit_rot_vel = 1500.0
        self.cactus_inv_hit_meter_bonus = 1.0
        self.invincible_bar_color1 = Color("#fcbad3")
        self.invincible_bar_color2 = Color("#a8d8ea")
        self.end_inv_shine_duration = 1

    def handle_event(self, event):
        if event.key == pygame.K_d:
            self.debug_rect = not self.debug_rect

    def close(self):
        # self.tkp.quit()
        pass
