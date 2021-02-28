import pygame
from entity import Entity
from SETTINGS import *


class Beam(pygame.sprite.Sprite):
    def __init__(self, source):
        super().__init__(beam_group, all_sprites)
        self.source = source
        self.rect = pygame.Rect(*self.source.hitbox.center, 10, 10)
        self.spawn_time = pygame.time.get_ticks()

    def detect_player(self):
        if pygame.time.get_ticks() - self.spawn_time > BEAM_LIIFETIME:
            self.kill()
            return False
        else:
            vec = pygame.Vector2
            rot = (vec(self.source.player.hitbox.center) - vec(self.source.hitbox.center)).angle_to(vec(1, 0))
            vel = vec(BEAM_SPEED, 0).rotate(-rot)
            self.rect.x += vel.x
            self.rect.y += vel.y
            if pygame.sprite.spritecollideany(self, walls_group):
                self.kill()
                return False
            if pygame.sprite.spritecollideany(self, player_group):
                self.kill()
                return True
        return None


class Enemy(Entity):
    def __init__(self, sheet, x, y, player):
        super().__init__(enemies_group)

        # Спрайт моба
        self.cut_sheet(sheet, 5, 5)
        self.image = self.frames[self.state][self.cur_frame]
        self.rect = self.rect.move(x * TILE_SIZE[0], y * TILE_SIZE[1])

        # Хитбокс моба
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        self.hitbox.center = self.rect.center

        self.player = player
        self.beam = Beam(self)
        self.player_already_detected = False

    def change_velocity(self):
        vec = pygame.Vector2
        rot = (vec(self.player.hitbox.center) - vec(self.hitbox.center)).angle_to(vec(1, 0))
        vel = vec(ENEMY_SPEED, 0).rotate(-rot)
        self.vx = vel.x
        self.vy = vel.y

    def move(self):
        if not self.player_already_detected:
            player_detected = self.beam.detect_player()
            if player_detected is not None:
                if player_detected:
                    self.change_velocity()
                    self.state = self.WALKING
                    self.player_already_detected = True
                    self.beam = None
                else:
                    self.vx = self.vy = 0
                    self.state = self.IDLE
                self.beam = Beam(self)
            super().move()
        else:
            self.change_velocity()
            self.state = self.WALKING
            super().move()

