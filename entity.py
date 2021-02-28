import pygame
from SETTINGS import *
import math


def collide_hitbox(one, two):
    # Функция нужна, чтобы столкновения рассчитовались не по rect, а по hitbox
    return one.hitbox.colliderect(two.rect)


class Entity(pygame.sprite.Sprite):
    # Константы состояния: стойка, удар, ходьба, оружие и смерть соответственно
    IDLE = 0
    PUNCH = 1
    WALKING = 2
    WEAPONS = 3
    DEATH = 4

    def __init__(self, group):
        # Текущее состояние
        super().__init__(group, all_sprites)
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
        # Текущий кадр
        self.cur_frame = 0

        # Текущая итерация главного цикла
        self.i = 1
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

    def update(self, target_pos):
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
            self.image = self.rotate(self.frames[self.state][self.cur_frame], target_pos)
            self.i = 0
        self.i += 1

    def rotate(self, image, target_pos):
        """Вычисляет угол поворота игрока относительно положения цели"""
        vector = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
        angle = (180 / math.pi) * math.atan2(vector[0], vector[1]) - 90
        image = pygame.transform.rotate(image, angle)
        # Получает новый прямоугольник из картинки
        self.rect = image.get_rect(center=self.rect.center)
        return image

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
        self.hitbox.centerx += self.vx
        self.collide_with_walls('x')
        self.hitbox.centery += self.vy
        self.collide_with_walls('y')
        self.rect.center = self.hitbox.center