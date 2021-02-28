import pygame


# screen = pygame.display.set_mode(SIZE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Размер (высота и ширина) - это размер экрана, если включен полноэкранный режим
SIZE = WIDTH, HEIGHT = pygame.display.get_window_size()
FPS = 60
# Скорость игрока
PLAYER_SPEED = 10
# Скорость врагов
ENEMY_SPEED = 7
# Скорость луча
BEAM_SPEED = 100
BEAM_LIIFETIME = 5000
# Скорость пули
BULLET_SPEED = 100
BULLET_LIFETIME = 500

# Размеры
PLAYER_SIZE = 100, 100
TILE_SIZE = 100, 100
HITBOX_SIZE = 50, 50
BULLET_SIZE = 10, 10

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
beam_group = pygame.sprite.Group()
player_bullets_group = pygame.sprite.Group()
enemies_bullets_group = pygame.sprite.Group()
