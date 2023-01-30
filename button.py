import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, filename, x, y, text):
        pg.sprite.Sprite.__init__(self)
        f = pg.font.Font(None, 64)
        self.image = pg.image.load(filename)
        self.message = text
        self.text = f.render(text, True, (0, 200, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def render(self, pre_screen):
        pre_screen.blit(self.image, self.rect)
        pre_screen.blit(self.text, self.rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
