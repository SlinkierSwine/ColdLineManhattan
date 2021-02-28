from entity import *


class Player(Entity):
    def __init__(self, sheet, x, y):
        """
        :param sheet: image (изображение спрайтов)
        :param x: float (первоначальные координаты)
        :param y: float (первоначальные координаты)
        """
        super().__init__(player_group)
        self.cut_sheet(sheet, 5, 5)
        self.image = self.frames[self.state][self.cur_frame]
        self.rect = self.rect.move(x * TILE_SIZE[0], y * TILE_SIZE[1])
        # Хитбокс игрока
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        self.hitbox.center = self.rect.center

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed(3)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.state = self.WALKING
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.state = self.WALKING
            self.vx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.state = self.WALKING
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.state = self.WALKING
            self.vy = PLAYER_SPEED
        # Чтобы по диагонали скорость была такая же, как и прямо
        # Умножаем скорости на 1 / sqrt(2)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if buttons[0]:
            self.state = self.PUNCH

    def move(self):
        self.get_keys()
        super().move()
