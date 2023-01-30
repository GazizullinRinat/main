import pygame as pg
import border


class Player(pg.sprite.Sprite):
    def __init__(self, coordinates):
        pg.sprite.Sprite.__init__(self)
        self.walkL = ['data/walking_1L.png', 'data/walking_2L.png', 'data/walking_3L.png', 'data/walking_4L.png',
                      'data/walking_5L.png', 'data/walking_6L.png', 'data/walking_7L.png', 'data/walking_8L.png']
        self.walkR = ['data/walking_1R.png', 'data/walking_2R.png', 'data/walking_3R.png', 'data/walking_4R.png',
                      'data/walking_5R.png', 'data/walking_6R.png', 'data/walking_7R.png', 'data/walking_8R.png']

        self.flyL = pg.transform.scale(pg.image.load('data/flyingL.png'), (128, 256))
        self.flyR = pg.transform.scale(pg.image.load('data/flyingR.png'), (128, 256))
        self.walking_anim_L = [pg.transform.scale(pg.image.load(i), (128, 256)) for i in self.walkL]
        self.walking_anim_R = [pg.transform.scale(pg.image.load(i), (128, 256)) for i in self.walkR]

        self.side = "L"
        self.acceleration = 0
        self.walking_num = 0
        self.walking = False
        self.flying = False
        self.sitting = False

        self.x, self.y = coordinates

        self.imageR = pg.image.load('data/stayR.png')
        self.imageR = pg.transform.scale(self.imageR, (128, 256))
        self.image = pg.image.load('data/stayL.png')
        self.image = pg.transform.scale(self.image, (128, 256))
        self.rect = self.image.get_rect(topright=(self.x, self.y))
        self.right_border = border.Border(self.rect.topright[0], 15 + self.rect.y, 1,
                                          self.rect.bottomright[1] - self.rect.y - 46)
        self.left_border = border.Border(self.rect.x, 15 + self.rect.y, 1,
                                         self.rect.bottomright[1] - self.rect.y - 46)
        self.up_border = border.Border(2 + self.rect.x, self.rect.y, self.x - self.rect.x - 4, 1)
        self.down_border = border.Border(2 + self.rect.x, self.rect.bottomright[1],
                                         self.rect.topright[0] - self.rect.x - 4, 1)

    def render_player(self, screen_, speed, coordinates_cam):
        self.rect.x -= coordinates_cam[0]
        self.rect.y -= coordinates_cam[1]
        if self.sitting:
            speed /= 2
        if self.flying:
            if self.side == "L":
                if self.sitting:
                    image = pg.transform.scale(self.flyL, (128, 128))
                else:
                    image = self.flyL
            else:
                if self.sitting:
                    image = pg.transform.scale(self.flyR, (128, 128))
                else:
                    image = self.flyR
        else:
            if self.walking:
                if self.side == "L":
                    if self.sitting:
                        image = pg.transform.scale(self.walking_anim_L[int(self.walking_num // 1)], (128, 128))
                    else:
                        image = self.walking_anim_L[int(self.walking_num // 1)]
                else:
                    if self.sitting:
                        image = pg.transform.scale(self.walking_anim_R[int(self.walking_num // 1)], (128, 128))
                    else:
                        image = self.walking_anim_R[int(self.walking_num // 1)]
                self.walking_num += speed
                self.walking_num %= 8
            else:
                if self.side == 'L':
                    if self.sitting:
                        image = pg.transform.scale(self.image, (128, 128))
                    else:
                        image = self.image
                else:
                    if self.sitting:
                        image = pg.transform.scale(self.imageR, (128, 128))
                    else:
                        image = self.imageR
        rect = image.get_rect(bottomright=self.rect.bottomright)
        screen_.blit(image, rect)

        self.rect.x += coordinates_cam[0]
        self.rect.y += coordinates_cam[1]

    def change(self):
        self.rect.topright = (self.x, self.y)
        self.right_border = border.Border(self.rect.topright[0], 15 + self.rect.y + 120 * self.sitting, 1,
                                          self.rect.bottomright[1] - self.rect.y - 46 - 120 * self.sitting)
        self.left_border = border.Border(self.rect.x, 15 + self.rect.y + 120 * self.sitting, 1,
                                         self.rect.bottomright[1] - self.rect.y - 46 - 120 * self.sitting)
        self.up_border = border.Border(4 + self.rect.x + 12 * self.flying, self.rect.y + 120 * self.sitting,
                                       self.x - self.rect.x - 8 - 12 * 2 * self.flying, 1)
        self.down_border = border.Border(16 + self.rect.x, self.rect.bottomright[1],
                                         self.rect.topright[0] - self.rect.x - 32, 1)

    def check_acc(self):
        if self.flying:
            self.acceleration += 0.7
        if abs(self.acceleration) < 0.5 or not self.flying:
            self.acceleration = 0

    def get_coord(self):
        return self.x, self.y
