import pygame
from SETTINGS import *
import math


class Player(pygame.sprite.Sprite):
    IDLE = 0
    PUNCH = 1
    WALKING = 2
    WEAPONS = 3
    DEATH = 4

    def __init__(self, sheet, x, y):
        super().__init__(player_group, all_sprites)
        self.state = self.IDLE
        self.states_imgs = {
            self.IDLE: 1,
            self.PUNCH: 4,
            self.WALKING: 4,
            self.WEAPONS: 5,
            self.DEATH: 2
        }
        self.frames = {}
        self.cut_sheet(sheet, 5, 5)
        self.cur_frame = 0
        self.image = self.frames[self.state][self.cur_frame]

        self.rect = self.rect.move(x * PLAYER_SIZE[0], y * PLAYER_SIZE[1])
        self.mask = pygame.mask.from_surface(self.image)

        self.i = 1
        self.mouse_pos = (0, 0)
        self.angle = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        ix = 0
        for key, value in self.states_imgs.items():
            for col in range(value):
                if not self.frames.get(key, False):
                    self.frames[key] = []
                # image = pygame.transform.scale(sheet.subsurface(pygame.Rect((self.rect.w * col, self.rect.h * ix), self.rect.size)), PLAYER_SIZE)
                image = sheet.subsurface(pygame.Rect((self.rect.w * col, self.rect.h * ix), self.rect.size))
                self.frames[key].append(image)
            ix += 1

    def update(self, mouse_pos):
        if self.i == 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.state])
            self.mouse_pos = mouse_pos
            self.image = self.rotate(self.frames[self.state][self.cur_frame], self.mouse_pos)
            self.i = 0
        self.i += 1

    def rotate(self, image, mouse_pos):
        vector = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        self.angle = (180 / math.pi) * math.atan2(vector[0], vector[1]) - 90
        image = pygame.transform.rotate(image, self.angle)
        self.rect = image.get_rect(center=self.rect.center)
        return image

    def move(self, key, mouse_pos):
        self.state = self.WALKING
        vec = pygame.Vector2(mouse_pos)
        pos = pygame.Vector2(self.rect.topleft)
        move = vec - pos
        if move.length() != 0:
            move.normalize_ip()
            if key == pygame.K_w:
                pos += move * SPEED
            elif key == pygame.K_s:
                pos -= move * SPEED
            self.rect.x = int(pos[0])
            # self.collide_with_walls('x', pos, move)
            self.rect.y = int(pos[1])
            # self.collide_with_walls('y', pos, move)

    def collide_with_walls(self, direction, pos, move):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, walls_group, False)
            print(hits)
            if hits:
                if move[0] > 0:
                    pos[0] = hits[0].rect.left - self.rect.width
                if move[0] < 0:
                    pos[0] = hits[0].rect.right
                self.rect.x = pos[0]
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, walls_group, False)
            print(hits)
            if hits:
                if move[1] > 0:
                    pos[1] = hits[0].rect.top - self.rect.h
                if move[1] < 0:
                    pos[1] = hits[0].rect.bottom
                self.rect.y = pos[1]

