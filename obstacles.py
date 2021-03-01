import pygame
from SETTINGS import *


class Obstacle(pygame.sprite.Sprite):
    """Класс стены"""
    def __init__(self, x, y, w, h):
        """
        :param x: float (Координаты стены)
        :param y: float (Координаты стены)
        """
        super().__init__(obstacles_group, all_sprites)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
