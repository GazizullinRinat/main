import pygame as pg


class Barrier(pg.sprite.Sprite):
    def __init__(self, filename, coordinates):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(filename), (128, 128))
        self.image.set_colorkey((255, 255, 255))
        self.coordinates = coordinates
        self.rect = self.image.get_rect(topleft=self.coordinates)

    def pre_render(self):
        self.rect = self.image.get_rect(topleft=self.coordinates)

    def render(self, screen_):
        screen_.blit(self.image, self.rect)
