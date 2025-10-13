import pygame
from random import randint


class Obstacle(object):
    def __init__(self, s, edge_range):
        self.s = s
        self.v = randint(56, 100)
        self.edge = randint(edge_range[0], edge_range[1])
        num = randint(0, 3)
        self.counter = 0
        self.enabled = True
        offset = randint(-30, 30)
        self.color = (159 + offset, 91 + offset, 58 + offset)
        x, y = 0, 0
        if num == 0 or num == 2:
            self.vy = 0
            if num == 0:
                y = self.s.cube_range[0]
            else:
                y = s.height - self.edge - self.s.cube_range[0]
            if randint(0, 1):
                self.vx = self.v
                x = -self.edge
            else:
                self.vx = -self.v
                x = s.width
        elif num == 1 or num == 3:
            self.vx = 0
            if num == 3:
                x = self.s.cube_range[0]
            else:
                x = s.width - self.edge - self.s.cube_range[0]
            if randint(0, 1):
                self.vy = self.v
                y = -self.edge
            else:
                self.vy = -self.v
                y = s.height
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, self.edge, self.edge)

    def update(self, pts, cube):
        if self.enabled:
            self.x += pts * self.vx
            self.y += pts * self.vy
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            if self.rect.colliderect(cube.rect):
                self.s.game_over = True
                pygame.time.set_timer(self.s.COUNT, 0)
            if self.counter > 100:
                if self.rect.top > self.s.height or self.rect.bottom < 0 or self.rect.left > self.s.width or self.rect.right < 0:
                    self.enabled = False
            self.counter += 1

    def display(self):
        if self.enabled:
            pygame.draw.rect(self.s.screen, self.color, self.rect, 0)
