"""
SID: 25098892g
NAME: LUO DONGPU

Cactus obstacle class.
"""

import pygame
from comp import GraphicComponent
from pygame.math import Vector2


class Cactus(GraphicComponent):
    def __init__(self, ctx, sprite, rect, vx, vy):
        super().__init__(ctx)
        self.is_active = True
        self.sprite = sprite
        self.rect = rect
        self.vx = vx
        self.vy = vy

        self.is_hit_by_invincible = False
        self.invincible_hit_dir: Vector2 = None
        self.inv_hit_rot: float = 0.0

    def update(self):

        if not self.is_active:
            return

        # update invincible hit movement
        pts = self.ctx.win.delta_time
        if self.is_hit_by_invincible:
            movement = self.invincible_hit_dir * self.ctx.cactus_inv_hit_speed * pts
            self.rect.move_ip(movement[0], movement[1])
            self.inv_hit_rot += self.ctx.cactus_inv_hit_rot_vel * pts
            self.inv_hit_rot %= 360
        else:
            # update normal movement
            vx = self.vx * self.ctx.mgr.cactus_speed_mul
            vy = self.vy * self.ctx.mgr.cactus_speed_mul
            self.rect.move_ip(pts * vx, pts * vy)
            if self.rect.colliderect(self.ctx.dino.col_rect):
                if self.ctx.mgr.invincible_mode:
                    self.is_hit_by_invincible = True
                    dir_x = self.rect.centerx - self.ctx.dino.col_rect.midbottom[0]+0.00001  # avoid 0-division
                    dir_y = self.rect.centery - self.ctx.dino.col_rect.midbottom[1]
                    self.invincible_hit_dir = Vector2(dir_x, dir_y).normalize()  # calculate hit direction
                    self.ctx.mgr.invincible_hit_cactus_bonus()  # get bonus
                else:
                    print("hit")
                    ...

        if not self.rect.colliderect(self.ctx.win.px_rect):  # out screen
            self.is_active = False
            return

    def render(self):
        if not self.is_active:
            return
        if self.is_hit_by_invincible:
            sprite = pygame.transform.rotate(self.sprite, self.inv_hit_rot)
        else:
            sprite = self.sprite
        self.ctx.win.display.blit(sprite, self.rect)
        if self.ctx.debug_rect:
            pygame.draw.rect(self.ctx.win.display, (0, 255, 0), self.rect, 1)
