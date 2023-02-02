import pygame as pg
import const, map_piece


class MapLayer(const.Const):
    def __init__(self, filename):
        super().__init__()
        f = open(filename)
        self.camera = [0, 0]
        self.sprites = pg.sprite.Group()
        self.cell_size = 128
        for i, line in enumerate(f.readlines()):
            for j, elem in enumerate(line.strip('\n').split(';')):
                if elem == "0":
                    continue
                for k in elem.split('/'):
                    print(k)
                    self.sprites.add(map_piece.Piece(self.types_interior.get(k), self.get_coordinates(i, j)))

    def get_coordinates(self, y, x):
        return x * self.cell_size, y * self.cell_size

    def render(self, screen_, coord):
        for sprite in self.sprites:
            sprite.rect.x -= coord[0]
            sprite.rect.y -= coord[1]
        self.sprites.draw(screen_)
        for sprite in self.sprites:
            sprite.rect.x += coord[0]
            sprite.rect.y += coord[1]