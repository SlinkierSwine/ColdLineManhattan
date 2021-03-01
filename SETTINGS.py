import pygame
from loads import *


# screen = pygame.display.set_mode(SIZE)
# Размер (высота и ширина) - это размер экрана, если включен полноэкранный режим
screen, clock, SIZE, WIDTH, HEIGHT = pygame_inits()

images = load_sprites()
groups = init_groups()
map_data = load_map()

# Настройки игрока
PLAYER_SPEED = 10
PLAYER_SIZE = 150, 150
HITBOX_SIZE = 50, 50
player_image = images[0]

# Настройки врагов
ENEMY_SPEED = 7
enemy_image = images[1]

# Настройки луча ботов
BEAM_SPEED = 20
BEAM_LIIFETIME = 5000

# Настройки пули
BULLET_SPEED = 20
BULLET_LIFETIME = 500
BULLET_RATE = 150
BULLET_SIZE = 10, 10
bullet_image = images[2]

FPS = 60

# Группы спрайтов
all_sprites = groups[0]
player_group = groups[1]
obstacles_group = groups[2]
enemies_group = groups[3]
beam_group = groups[4]
player_bullets_group = groups[5]
enemies_bullets_group = groups[6]

# Карта
level_map = map_data[0]
level_map_img = map_data[1]
level_map_rect = map_data[2]
