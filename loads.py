import pygame
import os
from map import Map


def load_image(*name, color_key=None):
    """Загружает картинку, если она существует
        Если ставить color_key=-1, то убирает фон картинки
    """
    fullname = os.path.join('data', 'imgs', *name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_sprites():
    # Спрайты игрока
    player_image = load_image('entity', 'sprite2.png', color_key=-1)
    # Спрайты врагов
    enemy_image = load_image('entity', 'enemies.png', color_key=-1)
    # Спрайт пули
    bullet_image = load_image('entity', 'bullet.png')
    return player_image, enemy_image, bullet_image,


def load_map():
    # Карта
    level_map = Map(os.path.join('data', 'maps', 'map.tmx'))
    level_map_img = level_map.make_map()
    level_map_rect = level_map_img.get_rect()
    return level_map, level_map_img, level_map_rect


def init_groups():
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    beam_group = pygame.sprite.Group()
    player_bullets_group = pygame.sprite.Group()
    enemies_bullets_group = pygame.sprite.Group()
    return all_sprites, player_group, obstacles_group, enemies_group, \
        beam_group, player_bullets_group, enemies_bullets_group


def pygame_inits():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    SIZE = WIDTH, HEIGHT = pygame.display.get_window_size()
    return screen, clock, SIZE, WIDTH, HEIGHT


def load_sounds():
    pygame.mixer.init()
    sounds = {
        'gunshot': pygame.mixer.Sound(os.path.join('data', 'sounds', 'gunshot.wav')),
        'footsteps': [pygame.mixer.Sound(os.path.join('data', 'sounds', 'footstep1.mp3')),
                     pygame.mixer.Sound(os.path.join('data', 'sounds', 'footstep2.mp3'))]
    }
    music = {
        'main theme': pygame.mixer.Sound(os.path.join('data', 'sounds', 'main theme.mp3'))
    }
    return sounds, music