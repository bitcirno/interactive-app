import pygame
from sys import exit
from random import randint
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE

from Cube import Cube
from Obstacle import Obstacle
from Timer import Timer

pygame.init()


class Screen(object):
    def __init__(self):
        self.width = 300
        self.height = self.width
        self.title = "cube jump"
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        pygame.event.set_allowed([QUIT, KEYDOWN])
        self.cube_range = [10, self.width - 10]

        # game manager
        self.COUNT = None
        self.game_over = False
        self.counter = 0
        self.next_c = randint(10, 20)
        self.next_c_range = [30, 60]
        self.obs = list()
        self.font = pygame.font.SysFont("Aria", 30)
        self.font2 = pygame.font.SysFont("Aria", 16)
        self.game_over_text = self.font.render("Game Over", True, (129, 59, 9))
        self.game_over_text_rect = self.game_over_text.get_rect(center=(self.width / 2, self.height / 2))
        self.restart_text = self.font2.render("Press space to restart", True, (149, 79, 29))
        self.restart_text_rect = self.restart_text.get_rect(center=(self.width / 2, self.height / 2 + 28))

        self.obs_edge_range = [8, 22]

    def update(self, pts, cube):
        self.__generate_obstacle(cube)
        self.__obs_update(pts, cube)

    def __generate_obstacle(self, cube):
        self.counter += 1
        if self.counter == self.next_c:
            for _ in range(3):
                self.obs.append(Obstacle(self, self.obs_edge_range))
            self.next_c = self.counter + randint(self.next_c_range[0], self.next_c_range[1])
        if self.counter == 300 or self.counter == 500 or self.counter == 700:
            self.next_c_range[0] -= 2
            self.next_c_range[1] -= 2
            self.obs_edge_range[0] += 2
            self.obs_edge_range[1] += 5
            cube.decrease_suspension_time()

    def __obs_update(self, pts, cube):
        for o in self.obs:
            o.update(pts, cube)
        for o in self.obs:
            if not o.enabled:
                self.obs.remove(o)

    def obs_display(self):
        for o in self.obs:
            o.display()
        if self.game_over:
            self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(self.restart_text, self.restart_text_rect)

    def restart_game(self, cube):
        cube.reset()
        self.game_over = False
        self.counter = 0
        self.next_c = randint(10, 20)
        self.next_c_range = [30, 60]
        self.obs = list()
        self.obs_edge_range = [8, 22]


s = Screen()
COUNT = pygame.USEREVENT + 1
s.COUNT = COUNT
fps = 60
timer = Timer(s, COUNT)
cube = Cube(s)
clock = pygame.time.Clock()
frame_color = (119, 49, 19)

while True:
    pt = clock.tick(fps)
    pts = pt / 1000.0
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            exit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                exit()
            if not s.game_over:
                if e.key == K_UP:
                    cube.to_up()
                elif e.key == K_DOWN:
                    cube.to_down()
                elif e.key == K_LEFT:
                    cube.to_left()
                elif e.key == K_RIGHT:
                    cube.to_right()
            else:
                if e.key == K_SPACE:
                    s.restart_game(cube)
                    timer.reset()

        if e.type == COUNT:
            timer.add_sec()

    if not s.game_over:
        cube.update(pts)
        timer.update_sec()
        s.update(pts, cube)

    s.screen.fill('white')
    if cube.suspend:
        cube.bar_display()
    s.obs_display()
    pygame.draw.rect(s.screen, frame_color, (0, 0, s.cube_range[0], s.height), 0)
    pygame.draw.rect(s.screen, frame_color, (s.cube_range[1], 0, s.cube_range[0], s.height), 0)
    pygame.draw.rect(s.screen, frame_color, (0, 0, s.width, s.cube_range[0]), 0)
    pygame.draw.rect(s.screen, frame_color, (0, s.cube_range[1], s.width, s.cube_range[0]), 0)
    timer.display_sec_text()
    cube.display()
    pygame.display.update()
