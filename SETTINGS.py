import pygame


# screen = pygame.display.set_mode(SIZE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SIZE = WIDTH, HEIGHT = pygame.display.get_window_size()
FPS = 60
SPEED = 10

PLAYER_SIZE = 100, 100
TILE_SIZE = 100, 100

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
