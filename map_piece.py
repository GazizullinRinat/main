import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, filename, coordinates):
        pg.sprite.Sprite.__init__(self)
        print(filename)
        image = pg.image.load(filename)
        self.image = pg.transform.scale(image, (128, 128))
        self.image.set_colorkey((255, 255, 255))
        self.coordinates = coordinates
        self.rect = self.image.get_rect(topleft=self.coordinates)

    def pre_render(self):
        self.rect = self.image.get_rect(topleft=self.coordinates)

    def render(self, screen_, coordinates_cam):
        self.rect.x -= coordinates_cam[0]
        self.rect.y -= coordinates_cam[1]
        screen_.blit(self.image, self.rect)
        pg.draw.rect(screen_, '#ff0000', (self.rect.x, self.rect.y, self.rect.bottomright[0] - self.rect.x,
                                          self.rect.bottomright[1] - self.rect.y), 1)
        self.rect.x += coordinates_cam[0]
        self.rect.y += coordinates_cam[1]
