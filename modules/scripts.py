import pygame
import sys
from modules.player import Player
from modules.obstacles import Obstacle
from modules.enemy import Enemy
from modules.loads import load_image
from SETTINGS import *


def terminate():
    pygame.quit()
    sys.exit()


def dropShadowText(screen, text, size, x, y, colour=(255, 255, 255), drop_colour=(0, 0, 0), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 2
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    # screen.blit(text_bitmap, (x+dropshadow_offset, y+dropshadow_offset) )
    _text = text_bitmap, (x+dropshadow_offset, y+dropshadow_offset)
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    _text_shadow = text_bitmap, (x, y)
    # screen.blit(text_bitmap, (x, y) )
    return _text, _text_shadow


def start_screen(screen, height):
    """Показывает начальный экран"""
    music['main theme'].set_volume(VOLUME)
    music['main theme'].play()
    bg = pygame.transform.scale(load_image('background', 'background.jpg'), SIZE)

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

    # Кнопка загрузки игры
    _button_start = pygame.Rect(
        400, _start_rect.y,
        200, 40
    )
    _button_start_shadow = pygame.Rect(
        (_button_start.x + 5, _button_start.y + 5), _button_start.size
    )

    # Текст "SETTINGS"
    _settings = font.render('SETTINGS', 1, pygame.Color('white'))
    _settings_rect = _settings.get_rect()
    _settings_rect.x = 200
    _settings_rect.y = _button_start.y + 90

    _settings_shadow = font.render('SETTINGS', 1, pygame.Color('black'))
    _settings_shadow_rect = _settings_shadow.get_rect()
    _settings_shadow_rect.x = _settings_rect.x + 2
    _settings_shadow_rect.y = _settings_rect.y + 2

    # Кнопка SETTINGS
    _button_settings = pygame.Rect(
        400, _settings_rect.y,
        200, 40
    )
    _button_settings_shadow = pygame.Rect(
        (_button_settings.x + 5, _button_settings.y + 5), _button_settings.size
    )

    # Текст "QUIT"
    _quit = font.render('QUIT', 1, pygame.Color('white'))
    _quit_rect = _quit.get_rect()
    _quit_rect.x = 200
    _quit_rect.y = _settings_rect.y + 90

    _quit_shadow = font.render('QUIT', 1, pygame.Color('black'))
    _quit_shadow_rect = _quit_shadow.get_rect()
    _quit_shadow_rect.x = _quit_rect.x + 2
    _quit_shadow_rect.y = _quit_rect.y + 2

    # Кнопка QUIT
    _button_quit = pygame.Rect(
        400, _quit_rect.y,
        200, 40
    )
    _button_quit_shadow = pygame.Rect(
        (_button_quit.x + 5, _button_quit.y + 5), _button_quit.size
    )

    state = 'main menu'

    while True:
        screen.blit(bg, bg.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            # Если нажали на кнопку - запустить игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if _button_start.collidepoint(event.pos) and state == 'main menu':
                    music['main theme'].stop()
                    return
                # if _button_settings.collidepoint(event.pos) and state == 'main menu':
                #     state = 'settings'
                if _button_quit.collidepoint(event.pos) and state == 'main menu':
                    terminate()
        if state == 'main menu':
            screen.blit(_start_shadow, _start_shadow_rect)
            screen.blit(_start, _start_rect)

            pygame.draw.rect(screen, pygame.Color('black'), _button_start_shadow)
            pygame.draw.rect(screen, pygame.Color('white'), _button_start)

            screen.blit(_settings_shadow, _settings_shadow_rect)
            screen.blit(_settings, _settings_rect)

            pygame.draw.rect(screen, pygame.Color('black'), _button_settings_shadow)
            pygame.draw.rect(screen, pygame.Color('white'), _button_settings)

            screen.blit(_quit_shadow, _quit_shadow_rect)
            screen.blit(_quit, _quit_rect)

            pygame.draw.rect(screen, pygame.Color('black'), _button_quit_shadow)
            pygame.draw.rect(screen, pygame.Color('white'), _button_quit)

        # elif state == 'settings':
        #     vol = dropShadowText(screen, 'VOLUME', 50, _start_rect.x, _start_rect.y)
        #     hun = dropShadowText(screen, '100', 50, _start_rect.x + 200, _start_rect.y)
        #     sev = dropShadowText(screen, '75', 50, _start_rect.x + 300, _start_rect.y)
        #     fif = dropShadowText(screen, '50', 50, _start_rect.x + 400, _start_rect.y)
        #     tw = dropShadowText(screen, '25', 50, _start_rect.x + 500, _start_rect.y)
        #     zero = dropShadowText(screen, '0', 50, _start_rect.x + 600, _start_rect.y)
        #     back = dropShadowText(screen, 'BACK', 50, _start_rect.x, _start_rect.y + 100)

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
