import pygame as pg


class LevelEnd(pg.sprite.Sprite):
    def __init__(self, filename, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename)
        self.rect = self.image.get_rect(center=(x, y))

    def render(self, screen_, coordinates_cam):
        self.rect.x -= coordinates_cam[0]
        self.rect.y -= coordinates_cam[1]
        screen_.blit(self.image, self.rect)
        self.rect.x += coordinates_cam[0]
        self.rect.y += coordinates_cam[1]

    def check(self, rect):
        return self.rect.colliderect(rect)
