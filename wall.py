import pygame
from SETTINGS import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(walls_group, all_sprites)
        self.image = pygame.transform.scale(image, TILE_SIZE)
        self.rect = self.image.get_rect().move(x * TILE_SIZE[0], y * TILE_SIZE[1])
        self.mask = pygame.mask.from_surface(self.image)


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(floor_group, all_sprites)
        self.image = pygame.transform.scale(image, TILE_SIZE)
        self.rect = self.image.get_rect().move(x * TILE_SIZE[0], y * TILE_SIZE[1])
        self.mask = pygame.mask.from_surface(self.image)
