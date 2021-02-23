import pygame
from SETTINGS import *


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(walls_group, all_sprites)
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.update()

    def update(self):
        pygame.draw.rect(screen, [0, 0, 0], self.rect)
