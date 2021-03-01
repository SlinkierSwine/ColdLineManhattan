from SETTINGS import *


class Camera:
    """Класс камеры"""
    def __init__(self):
        # Начальный сдвиг камеры
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        """Сдвигает объект obj на сдвиг камеры"""
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def apply_rect(self, rect):
        rect.x += self.dx
        rect.y += self.dy

    def update(self, target):
        """Позиционирует камеру на объекте target"""
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
