import pygame as pg


class Border(pg.sprite.Sprite):
    def __init__(self, x, y, x1, y1):
        pg.sprite.Sprite.__init__(self)
        self.surf = pg.Surface([0, 0])
        self.rect = pg.Rect(x, y, x1, y1)

    def change(self, x, y):
        self.rect.x -= x
        self.rect.y -= y

    def rechange(self, x, y):
        self.rect.x += x
        self.rect.y += y
