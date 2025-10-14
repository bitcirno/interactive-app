"""
SID: 25098892g
NAME: LUO DONGPU

Main entrance of the game.
"""

import pygame
from random import randint

from context import Context
from manager import Manager
from win import PixelGameWindow
from dinosaur import Dino
from ground import Ground
from tween import Tween
from timer import Timer


pygame.init()
# pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

ctx = Context()
win = PixelGameWindow(ctx, (240, 240), (540, 540), "4xDinosaur", 60)
mgr = Manager(ctx)
dino = Dino(ctx)
timer = Timer(ctx)
ground = Ground(ctx)

mgr.bind_timer_events(timer)

timer.restart_round()


while True:

    # early update of a frame
    win.early_update()

    # handle events
    is_running = True
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                is_running = False
                break
            ctx.handle_event(event)
            dino.handle_event(event)

    if not is_running:
        break

    # update game components
    mgr.update()
    timer.update()
    ground.update()
    dino.update()

    # update active tweens
    Tween.update_active_tweens()

    # render game components
    timer.render()
    ground.render()
    mgr.render_cactus()
    dino.render()
    mgr.render_top_shine()

    # final blit event by visual window
    win.final_blit_event()


# quit application
win.quit()
pygame.quit()
ctx.close()
print(f"{'[App]': <8} Quit")
