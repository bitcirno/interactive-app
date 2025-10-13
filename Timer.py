import pygame


class Timer(object):
    def __init__(self, s, COUNT):
        self.s = s
        self.sec = 0
        self.counter = 0
        self.COUNT = COUNT
        pygame.time.set_timer(COUNT, 1000)
        self.font = pygame.font.SysFont("Aria", 16)
        self.sec_text = self.font.render(f"Time: {self.sec}", True, (50, 50, 50))
        self.sec_text_rect = self.sec_text.get_rect(center=(self.s.width / 2, self.s.height / 9))

    def add_sec(self):
        self.sec += 1
        self.counter = 0

    def update_sec(self):
        if self.counter < 10:
            counter_text = '0' + str(self.counter)
        else:
            counter_text = str(self.counter)
        self.sec_text = self.font.render(f"Time: {self.sec}.{counter_text}", True, (50, 50, 50))
        self.sec_text_rect = self.sec_text.get_rect(center=(self.s.width / 2, self.s.height / 9))
        self.counter += 1

    def display_sec_text(self):
        self.s.screen.blit(self.sec_text, self.sec_text_rect)

    def reset(self):
        self.sec = 0
        self.counter = 0
        pygame.time.set_timer(self.COUNT, 1000)
