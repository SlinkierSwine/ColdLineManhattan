import pygame
from SETTINGS import *
from camera import Camera
from scripts import *


pygame.init()
pygame.key.set_repeat(1, 25)
pygame.display.set_caption('ColdLine Manhattan')

start_screen(screen, HEIGHT)
start_time = pygame.time.get_ticks()

running = True

player = generate_level(level_map, player_image, enemy_image)
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

    player.move()
    for enemy in enemies_group:
        enemy.move()

    screen.fill(pygame.Color(82, 0, 89))

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

    camera.apply_rect(level_map_rect)
    screen.blit(level_map_img, level_map_rect)

    hits = pygame.sprite.groupcollide(enemies_group, player_bullets_group, False, True)
    for hit in hits:
        hit.kill()

    # hits = pygame.sprite.groupcollide(player_group, enemies_bullets_group, False, True)
    # if hits:
    #     player.state = player.DEATH
    #     running = False
    #     game_over_screen(screen, WIDTH, HEIGHT)

    if len(enemies_group) == 0:
        running = False
        finish_time = pygame.time.get_ticks()
        all_time = finish_time - start_time
        win_screen(screen, WIDTH, HEIGHT, all_time)

    # Отрисовка спрайтов
    player_group.draw(screen)
    enemies_group.draw(screen)
    player_bullets_group.draw(screen)
    enemies_bullets_group.draw(screen)
    # pygame.draw.rect(screen, (0, 0, 0), player.hitbox, 2)
    # for e in enemies_group:
    #     pygame.draw.rect(screen, (0, 0, 0), e.hitbox, 2)
    # for b in beam_group:
    #     pygame.draw.rect(screen, (0, 0, 0), b.rect)

    # Обновление спрайтов
    player.update(pygame.mouse.get_pos())
    enemies_group.update(player.rect.center)
    player_bullets_group.update()
    enemies_bullets_group.update()
    obstacles_group.update()

    # Фпс в углу экрана
    font = pygame.font.Font(None, 30)
    fps = font.render(f'FPS: {int(clock.get_fps())}', 1, pygame.Color('red'))
    fps_rect = fps.get_rect()
    screen.blit(fps, fps_rect)

    # Время
    font = pygame.font.Font(None, 75)
    now = pygame.time.get_ticks()

    time = font.render(f'Time: {round((now - start_time) / 1000, 1)}s', 1, pygame.Color('white'))
    time_rect = time.get_rect()
    time_rect = time_rect.move(WIDTH - time_rect.width - 20, 10)

    time_shadow = font.render(f'Time: {round((now - start_time) / 1000, 1)}s', 1, pygame.Color('black'))
    time_shadow_rect = time_shadow.get_rect()
    time_shadow_rect = time_shadow_rect.move(time_rect.x + 2, time_rect.y + 2)

    screen.blit(time_shadow, time_shadow_rect)
    screen.blit(time, time_rect)

    pygame.display.flip()
    clock.tick(FPS)
