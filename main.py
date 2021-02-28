import pygame
import sys
import os
from SETTINGS import *
from player import Player
from wall import Wall, Floor
from camera import Camera
from enemy import Enemy
from map import Map


pygame.init()
pygame.key.set_repeat(1, 25)
pygame.display.set_caption('ColdLine Manhattan')


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


def load_level(filename):
    """Загружает уровень из текстового файла"""
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
    """Показывает начальный экран"""
    bg = load_image('background', 'background.jpg')
    screen.blit(bg, bg.get_rect())
    font = pygame.font.Font(None, 50)
    # Текст "START"
    _start = font.render('START', 1, pygame.Color('white'))
    _start_rect = _start.get_rect()
    _start_rect.x = 200
    _start_rect.y = (HEIGHT - _start_rect.height) // 2

    _start_shadow = font.render('START', 1, pygame.Color('black'))
    _start_shadow_rect = _start_shadow.get_rect()
    _start_shadow_rect.x = _start_rect.x + 2
    _start_shadow_rect.y = _start_rect.y + 2

    screen.blit(_start_shadow, _start_shadow_rect)
    screen.blit(_start, _start_rect)

    # Кнопка загрузки игры
    _button = pygame.Rect(
        180, (HEIGHT - 40) // 2 + 60,
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
            clock.tick(FPS)


def generate_level(level_map):
    """Генерирует уровень, в котором w - стена, . - пустое пространство(пол), @ - игрок"""
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == 'w':
                Wall(x, y, wall_image)
            elif level_map[y][x] == '.':
                Floor(x, y, floor_image)
            elif level_map[y][x] == '@':
                Floor(x, y, floor_image)
                new_player = Player(player_image, x, y, bullet_image)
            elif level_map[y][x] == 'M':
                Floor(x, y, floor_image)
                Enemy(enemy_image, x, y, new_player, Enemy.PISTOL, bullet_image)
        # вернем игрока, а также размер поля в клетках
    return new_player, x, y


start_screen()

running = True
# Спрайты игрока
player_image = load_image('entity', 'sprite2.png', color_key=-1)
# Спрайты стены
# wall_image = load_image('new wall.png')
# Спрайты пола
# floor_image = load_image('floor.png')
# Спрайты врагов
enemy_image = load_image('entity', 'enemies.png', color_key=-1)
# Спрайт пули
bullet_image = load_image('entity', 'bullet.png')

new_map = Map(os.path.join('data', 'maps', 'map.tmx'))
map_img = new_map.make_map()
map_rect = map_img.get_rect()

player = Player(player_image, 10, 10, bullet_image)

# player, field_x, field_y = generate_level(load_level('test_map'))
for enemy in enemies_group:
    enemy.player = player
camera = Camera()

while running:
    # Делает курсор прицелом
    try:
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
    except:
        pygame.mouse.set_cursor(pygame.cursors.arrow)
    wasd_arrows_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                terminate()
        if event.type == pygame.KEYUP:
            player.state = player.IDLE
        if event.type == pygame.MOUSEBUTTONDOWN and player.weapon == player.PISTOL or player.weapon == player.RIFLE:
            player.state = player.PISTOL
            player.shoot(pygame.mouse.get_pos(), player_bullets_group)

    player.move()

    for enemy in enemies_group:
        enemy.move()

    screen.fill(pygame.Color(255, 255, 255))

    # Сдвиг камеры
    camera.update(player)
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            player.hitbox.x += camera.dx
            player.hitbox.y += camera.dy
        elif isinstance(sprite, Enemy):
            sprite.hitbox.x += camera.dx
            sprite.hitbox.y += camera.dy
        else:
            camera.apply(sprite)

    camera.apply_rect(map_rect)
    screen.blit(map_img, map_rect)

    hits = pygame.sprite.groupcollide(enemies_group, player_bullets_group, False, True)
    for hit in hits:
        hit.kill()

    # Отрисовка спрайтов
    walls_group.draw(screen)
    floor_group.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)
    player_bullets_group.draw(screen)
    enemies_bullets_group.draw(screen)
    pygame.draw.rect(screen, (0, 0, 0), player.hitbox, 2)
    for e in enemies_group:
        pygame.draw.rect(screen, (0, 0, 0), e.hitbox, 2)
    for b in beam_group:
        pygame.draw.rect(screen, (0, 0, 0), b.rect)

    # Высчитывание поворота игрока
    player.update(pygame.mouse.get_pos())
    enemies_group.update(player.rect.center)
    player_bullets_group.update()
    enemies_bullets_group.update()

    # Фпс в углу экрана
    font = pygame.font.Font(None, 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', 1, pygame.Color('red'))
    fps_rect = fps.get_rect()
    screen.blit(fps, fps_rect)

    # Позиция игрока и хитбокса игрока
    pos = font.render(str(map_rect), 1, pygame.Color('red'))
    pos_rect = pos.get_rect()
    screen.blit(pos, (pos_rect.x + 100, pos_rect.y))

    pygame.display.flip()
    clock.tick(FPS)
