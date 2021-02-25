import pygame
import sys
import os
from SETTINGS import *
from player import Player
from wall import Wall, Floor
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


def load_level(filename):
    filename = os.path.join('data', 'maps', filename)
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill(pygame.Color(0, 0, 0))
    font = pygame.font.Font(None, 30)
    _start = font.render('START', 1, pygame.Color('white'))
    _start_rect = _start.get_rect()
    _start_rect.x = (WIDTH - _start_rect.width) // 2
    _start_rect.y = (HEIGHT - _start_rect.height) // 2 - 60

    screen.blit(_start, _start_rect)

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


def generate_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == 'w':
                Wall(x, y, wall_image)
            elif level_map[y][x] == '.':
                Floor(x, y, floor_image)
            elif level_map[y][x] == '@':
                Floor(x, y, floor_image)
                new_player = Player(player_image, x, y)
        # вернем игрока, а также размер поля в клетках
    return new_player, x, y


start_screen()

running = True
player_image = load_image('sprite2.png', -1)
punch_image = load_image('punch.png')
wall_image = load_image('new wall.png')
floor_image = load_image('floor.png')
player, a, ad = generate_level(load_level('test_map'))
camera = Camera()

while running:
    pygame.mouse.set_cursor(pygame.cursors.broken_x)
    old_x = player.rect.x
    old_y = player.rect.y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                terminate()
            if event.key == pygame.K_w:
                player.move(pygame.K_w, pygame.mouse.get_pos())
            if event.key == pygame.K_s:
                player.move(pygame.K_s, pygame.mouse.get_pos())
        if event.type == pygame.KEYUP:
            player.state = Player.IDLE

    for wall in walls_group:
        if pygame.sprite.collide_mask(player, wall):
            player.rect.x = old_x
            player.rect.y = old_y

    # for tile in pygame.sprite.spritecollide(player, walls_group, False):
    #     player.rect.x = old_x
    #     player.rect.y = old_y
    screen.fill(pygame.Color(255, 255, 255))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    walls_group.draw(screen)
    floor_group.draw(screen)
    player_group.draw(screen)
    player.update(pygame.mouse.get_pos())

    font = pygame.font.Font(None, 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', 1, pygame.Color('red'))
    fps_rect = fps.get_rect()
    screen.blit(fps, fps_rect)

    pygame.display.flip()
    clock.tick(FPS)
