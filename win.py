"""
SID: 25098892g
NAME: LUO DONGPU

Game window
"""

import pygame
from pygame.surface import Surface
from pygame.color import Color
import pygame_shaders
from pygame_shaders import Shader
import time


class PixelGameWindow:
    def __init__(self, ctx,
                 px_reso: tuple = (60, 60),
                 full_reso: tuple = (540, 540),
                 title: str = "4xDinosaur",
                 fps: int = 60):

        self.ctx = ctx
        self.ctx.win = self
        self.resolution: tuple = px_reso
        self.full_resolution: tuple = full_reso
        self.title: str = title
        self.fps: int = fps

        pygame.display.set_mode(full_reso, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(f"{title}  FPS: {fps}")

        self.display: Surface = Surface(px_reso)
        self.clock = pygame.time.Clock()
        self.app_time: float = 0  # accumulated time since app start
        self.delta_time: float = 0  # time since last frame
        self.clear_display_color = Color(255, 255, 255)

        self.px_rect = self.display.get_rect()
        self.full_rect = pygame.Rect(0, 0, full_reso[0], full_reso[1])
        self.__screen_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "shaders/crt_post.glsl", self.display)
        self.__screen_shader.send("resolution", px_reso)
        # self.__screen_shader.send("speed", 3)
        self.__app_start_time: float = time.time()

        # events
        self.is_left_pointer_down: bool = False  # is pointer down this frame?

        # real-time fps calculation
        self.fps_accum_target: int = 10
        self.fps_accum_count: int = 0
        self.fps_accum_time: float = 0.0
        self.smoothed_fps: int = fps

    def handle_event(self, event):
        self.is_left_pointer_down = False
        if event.button == 1:
            self.is_left_pointer_down = True

    def __calculate_smooth_fps(self):
        self.fps_accum_count += 1
        self.fps_accum_time += self.delta_time
        if self.fps_accum_count >= self.fps_accum_target:
            self.smoothed_fps = round(self.fps_accum_count / self.fps_accum_time)
            pygame.display.set_caption(f"{self.title}  FPS: {self.smoothed_fps}")
            self.fps_accum_count = 0
            self.fps_accum_time = 0.0

    def early_update(self):
        """
        Update import data (time etc) at first of a frame
        """
        self.display.fill(self.clear_display_color)
        self.app_time = time.time() - self.__app_start_time
        self.delta_time = self.clock.get_time() / 1000.0
        self.__calculate_smooth_fps()

    def final_blit_event(self):
        self.__screen_shader.render_direct(self.full_rect)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pass
