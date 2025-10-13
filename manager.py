"""
SID: 25098892g
NAME: LUO DONGPU

Game manager module controlling the game rules and flow
"""

from context import Context
from random import randint


class Manager(object):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.ctx.mgr = self
        self.width = 300
        self.height = self.width
        self.title = "cube jump"
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
