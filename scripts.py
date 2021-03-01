import pygame
import sys
from player import Player
from obstacles import Obstacle
from enemy import Enemy
from loads import load_image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen, height):
    """Показывает начальный экран"""
    bg = load_image('background', 'background.jpg')
    screen.blit(bg, bg.get_rect())
    font = pygame.font.Font(None, 50)
    # Текст "START"
    _start = font.render('START', 1, pygame.Color('white'))
    _start_rect = _start.get_rect()
    _start_rect.x = 200
    _start_rect.y = (height - _start_rect.height) // 2

    _start_shadow = font.render('START', 1, pygame.Color('black'))
    _start_shadow_rect = _start_shadow.get_rect()
    _start_shadow_rect.x = _start_rect.x + 2
    _start_shadow_rect.y = _start_rect.y + 2

    screen.blit(_start_shadow, _start_shadow_rect)
    screen.blit(_start, _start_rect)

    # Кнопка загрузки игры
    _button = pygame.Rect(
        180, (height - 40) // 2 + 60,
        150, 40
    )
    _button_shadow = pygame.Rect(
        (_button.x + 5, _button.y + 5), _button.size
    )
    pygame.draw.rect(screen, pygame.Color('black'), _button_shadow)
    pygame.draw.rect(screen, pygame.Color('white'), _button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # Если нажали на кнопку - запустить игру
            elif event.type == pygame.MOUSEBUTTONDOWN and _button.collidepoint(event.pos):
                return
            pygame.display.flip()


def game_over_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    # Текст "Game over"
    _over = font.render('GAME OVER', 1, pygame.Color('white'))
    _over_rect = _over.get_rect()
    _over_rect.x = (width - _over_rect.width) // 2
    _over_rect.y = (height - _over_rect.height) // 2

    screen.blit(_over, _over_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            pygame.display.flip()


def win_screen(screen, width, height, time):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    # Текст "Game over"
    _over = font.render('YOU WON!', 1, pygame.Color('white'))
    _over_rect = _over.get_rect()
    _over_rect.x = (width - _over_rect.width) // 2
    _over_rect.y = (height - _over_rect.height) // 2

    _time = font.render(f'Your time: {round(time / 1000, 2)}s', 1, pygame.Color('white'))
    _time_rect = _time.get_rect()
    _time_rect.x = (width - _time_rect.width) // 2
    _time_rect.y = (height - _time_rect.height) // 2 + 100

    screen.blit(_over, _over_rect)
    screen.blit(_time, _time_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            pygame.display.flip()


def generate_level(level_map, player_image, enemy_image):
    """Генерирует уровень, в котором w - стена, . - пустое пространство(пол), @ - игрок"""
    player = None
    for tile_object in level_map.tmxdata.objects:
        if tile_object.name == 'Player':
            player = Player(player_image, tile_object.x, tile_object.y)
        if tile_object.name == 'Obstacle':
            Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        if tile_object.name == 'Mob':
            Enemy(enemy_image, tile_object.x, tile_object.y, player, Enemy.PISTOL)
    return player
