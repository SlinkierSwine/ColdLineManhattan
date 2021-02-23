import pygame
from SETTINGS import *
import math


class Player(pygame.sprite.Sprite):
    idle = 0
    walking = 1

    def __init__(self, sheet):
        super().__init__(player_group, all_sprites)
        self.state = self.idle
        self.frames = {}
        self.cut_sheet(sheet, 6, 1)
        self.cur_frame = 0
        self.image = self.frames[self.state][self.cur_frame]

        self.rect = self.rect.move((WIDTH - self.rect.w) // 2, (HEIGHT - self.rect.h) // 2)

        self.i = 1
        self.mouse_pos = (0, 0)
        self.angle = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if i == 0:
                    if not self.frames.get(self.idle, False):
                        self.frames[self.idle] = []
                    self.frames[self.idle].append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
                elif i >= 1:
                    if not self.frames.get(self.walking, False):
                        self.frames[self.walking] = []
                    self.frames[self.walking].append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

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

