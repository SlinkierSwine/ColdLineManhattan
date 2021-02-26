import pygame
from SETTINGS import *


class Wall(pygame.sprite.Sprite):
    """Класс стены"""
    def __init__(self, x, y, image):
        """
        :param x: float (Координаты стены)
        :param y: float (Координаты стены)
        :param image: image (Изображение стены)
        """
        super().__init__(walls_group, all_sprites)
        # Подгоняет изображение под размер одной плитки
        self.image = pygame.transform.scale(image, TILE_SIZE)
        self.rect = self.image.get_rect().move(x * TILE_SIZE[0], y * TILE_SIZE[1])
        # Маска стены
        self.mask = pygame.mask.from_surface(self.image)


class Floor(pygame.sprite.Sprite):
    """Класс пола"""
    def __init__(self, x, y, image):
        """
        :param x: float (Координаты пола)
        :param y: float (Координаты пола)
        :param image: image (Изображение пола)
        """
        super().__init__(floor_group, all_sprites)
        # Подгоняет изображение под размер одной плитки
        self.image = pygame.transform.scale(image, TILE_SIZE)
        self.rect = self.image.get_rect().move(x * TILE_SIZE[0], y * TILE_SIZE[1])
