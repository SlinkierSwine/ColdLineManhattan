from player import *


class Enemy(Player):
    def __init__(self, sheet, x, y):
        super().__init__(sheet, x, y)
        pygame.sprite.Sprite.__init__(enemies_group, all_sprites)
        self.cut_sheet(sheet, 5, 5)
        self.image = self.frames[self.state][self.cur_frame]
        self.rect = self.image.get_rect()
