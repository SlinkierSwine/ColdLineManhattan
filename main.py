import pygame
import sys
import os
from SETTINGS import *
from player import Player
from walls import Wall
from camera import Camera


pygame.init()
pygame.key.set_repeat(1, 25)
pygame.display.set_caption('ColdLine Manhattan')


def load_image(name, color_key=None):
    fullname = os.path.join('data', 'imgs', name)
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill(pygame.Color(0, 0, 0))
    font = pygame.font.Font(None, 30)
    _level = font.render('START', 1, pygame.Color('white'))
    _level_rect = _level.get_rect()
    _level_rect.x = (WIDTH - _level_rect.width) // 2
    _level_rect.y = (HEIGHT - _level_rect.height) // 2 - 60

    screen.blit(_level, _level_rect)

    _button = pygame.Rect(
        (WIDTH - 150) // 2, (HEIGHT - 40) // 2,
        150, 40
    )
    pygame.draw.rect(screen, [255, 255, 255], _button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and _button.collidepoint(event.pos):
                return
            pygame.display.flip()
            clock.tick(FPS)


start_screen()

running = True
player_image = load_image('sprite_player.png', -1)
player = Player(player_image)
wall = Wall()
camera = Camera()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            player.state = Player.walking
            if event.key == pygame.K_w:
                vec = pygame.Vector2(pygame.mouse.get_pos())
                pos = pygame.Vector2(player.rect.topleft)
                move = vec - pos
                if move.length() != 0:
                    move.normalize_ip()
                    pos += move * SPEED
                    player.rect.topleft = list(int(v) for v in pos)
        if event.type == pygame.KEYUP:
            player.state = Player.idle
    screen.fill(pygame.Color(255, 255, 255))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player_group.draw(screen)
    wall.update()
    player.update(pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(FPS)
