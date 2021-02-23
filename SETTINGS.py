import pygame


SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
SPEED = 10

screen = pygame.display.set_mode(SIZE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
