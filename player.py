import pygame
from SETTINGS import *
import math


def collide_hitbox(one, two):
    # Функция нужна, чтобы столкновения рассчитовались не по rect, а по hitbox
    return one.hitbox.colliderect(two.rect)


class Player(pygame.sprite.Sprite):
    # Константы состояния: стойка, удар, ходьба, оружие и смерть соответственно
    IDLE = 0
    PUNCH = 1
    WALKING = 2
    WEAPONS = 3
    DEATH = 4

    def __init__(self, sheet, x, y):
        """
        :param sheet: image (изображение спрайтов)
        :param x: float (первоначальные координаты)
        :param y: float (первоначальные координаты)
        """
        super().__init__(player_group, all_sprites)
        # Текущее состояние
        self.state = self.IDLE
        # Количество картинок определенных спрайтов в листе спрайтов
        self.states_imgs = {
            self.IDLE: 1,
            self.PUNCH: 4,
            self.WALKING: 4,
            self.WEAPONS: 5,
            self.DEATH: 2
        }
        # Спрайты каждого состояния (вызываются по константам состяния), словарь списков
        self.frames = {}
        self.cut_sheet(sheet, 5, 5)
        # Текущий кадр
        self.cur_frame = 0
        self.image = self.frames[self.state][self.cur_frame]

        self.rect = self.rect.move(x * TILE_SIZE[0], y * TILE_SIZE[1])
        # Хитбокс игрока
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        self.hitbox.center = self.rect.center

        # Текущая итерация главного цикла
        self.i = 1
        # Позиция мышки
        self.mouse_pos = (0, 0)
        # Текущий угол поворота игрока
        self.angle = 0
        # Проекции скорости
        self.vx = self.vy = 0

    def cut_sheet(self, sheet, columns, rows):
        """Разрезает спрайт лист на отдельные спрайты в словаре frames"""
        # Хитбокс размером с картинку спрайта
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        ix = 0
        for key, value in self.states_imgs.items():
            for col in range(value):
                if not self.frames.get(key, False):
                    self.frames[key] = []
                # image = pygame.transform.scale(sheet.subsurface(pygame.Rect((self.rect.w * col, self.rect.h * ix), self.rect.size)), PLAYER_SIZE)
                image = sheet.subsurface(pygame.Rect((self.rect.w * col, self.rect.h * ix), self.rect.size))
                self.frames[key].append(image)
            ix += 1
        # Удар проигрывается сначала в одном направлении, потом обратно
        self.frames[self.PUNCH] += self.frames[self.PUNCH][::-1]

    def update(self, mouse_pos):
        """Изменяет текущий спрайт на следующий и поворачивает его на нужный угол"""
        if self.i == 3:
            # Удар проигрывается сначала в одном направлении, потом обратно
            if self.state == self.PUNCH:
                if self.cur_frame < len(self.frames[self.PUNCH]) - 1:
                    self.cur_frame = self.cur_frame + 1
                else:
                    self.state = self.IDLE
                    self.cur_frame = 0
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.state])
            self.mouse_pos = mouse_pos
            self.image = self.rotate(self.frames[self.state][self.cur_frame], self.mouse_pos)
            self.i = 0
        self.i += 1

    def rotate(self, image, mouse_pos):
        """Вычисляет угол поворота игрока относительно положения мыши"""
        vector = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        self.angle = (180 / math.pi) * math.atan2(vector[0], vector[1]) - 90
        image = pygame.transform.rotate(image, self.angle)
        # Получает новый прямоугольник из картинки
        self.rect = image.get_rect(center=self.rect.center)
        return image

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.state = self.WALKING
            self.vx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.state = self.WALKING
            self.vx = SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.state = self.WALKING
            self.vy = -SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.state = self.WALKING
            self.vy = SPEED
        # Чтобы по диагонали скорость была такая же, как и прямо
        # Умножаем скорости на 1 / sqrt(2)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, direction):
        # Столкновения по х
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, walls_group, False, collide_hitbox)
            if hits:
                if self.vx > 0:
                    self.hitbox.centerx = hits[0].rect.left - self.hitbox.width / 2
                if self.vx < 0:
                    self.hitbox.centerx = hits[0].rect.right + self.hitbox.width / 2
                self.vx = 0
        # Столкновения по у
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, walls_group, False, collide_hitbox)
            if hits:
                if self.vy > 0:
                    self.hitbox.centery = hits[0].rect.top - self.hitbox.height / 2
                if self.vy < 0:
                    self.hitbox.centery = hits[0].rect.bottom + self.hitbox.height / 2
                self.vy = 0

    def move(self):
        # Проверяем столкновения хитбокса, а затем присваеваем его координаты к игроку
        self.get_keys()
        self.hitbox.centerx += self.vx
        self.collide_with_walls('x')
        self.hitbox.centery += self.vy
        self.collide_with_walls('y')
        self.rect.center = self.hitbox.center

