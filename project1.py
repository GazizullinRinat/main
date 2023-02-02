import pygame as pg
import const, player, map_piece, level_end, map_layer, user_interface
import sys


class Board(const.Const):
    def __init__(self):
        super().__init__()
        self.sprites = pg.sprite.Group()
        self.cell_size = 128
        self.end = []
        self.x, self.y = 0, 0

    def open(self, filename):
        f = open(filename)
        self.cell_size = 128
        self.x, self.y = 0, 0
        self.sprites = pg.sprite.Group()
        for i, line in enumerate(f.readlines()):
            for j, elem in enumerate(line.strip('\n').split(';')):
                if elem == '2':
                    continue
                elif elem == '0':
                    self.x, self.y = j, i
                    continue
                elif elem == "3":
                    self.level_end_coordinations = list(self.get_coordinates(i, j, add=self.cell_size // 2))
                    continue
                self.sprites.add(map_piece.Piece(self.sprite_filenames.get(elem),
                                                 self.get_coordinates(i, j)))

    def get_coordinates(self, y, x, add=0):
        return x * self.cell_size + add, y * self.cell_size + add

    def render_map(self, screen_, coord):
        for sprite in self.sprites:
            sprite.rect.x -= coord[0]
            sprite.rect.y -= coord[1]
        self.sprites.draw(screen_)
        for sprite in self.sprites:
            sprite.rect.x += coord[0]
            sprite.rect.y += coord[1]


class Game(Board, user_interface.Pause, user_interface.Menu):
    def __init__(self):
        f = open("data/levels.txt")
        Board.__init__(self)
        self.levels = list(map(lambda x: x.strip('\n').split(";"), f.readlines()))
        self.menu = user_interface.Menu(list(map(lambda x: x[0], self.levels)))
        self.pause = user_interface.Pause()
        self.info = pg.display.Info()
        self.special_info = False
        self.end = False
        self.passed = False
        self.playing = False
        self.is_menu = True
        self.paused = False

    def end_level(self):
        self.is_menu = True
        self.paused = False
        self.playing = False

    def change_level(self, level_name):
        self.is_menu = False
        self.paused = False
        self.playing = True
        
        for i in self.levels:
            if i[0] == level_name:
                self.open(i[1])
                self.interior = map_layer.MapLayer(i[2])
                self.back = map_layer.MapLayer(i[3])
        self.level_end = level_end.LevelEnd("data/level_end.png", self.level_end_coordinations[0],
                                            self.level_end_coordinations[1])
        self.coordinates_player = self.get_coordinates(self.y - 1, self.x + 1)
        self.player = player.Player(self.coordinates_player)
        self.camera_coordinates = [-abs(self.player.rect.centerx - self.info.current_w // 2),
                                   abs(-self.info.current_h // 2 + self.player.rect.centery)]
        self.speed = 0.125
        self.respawn_coordinates = self.coordinates_player
        self.camera_respawn = self.camera_coordinates.copy()

    def render(self, pre_screen):
        if self.playing:
            self.back.render(pre_screen, self.camera_coordinates)
            self.render_map(pre_screen, self.camera_coordinates)
            self.interior.render(pre_screen, self.camera_coordinates)
            self.player.render_player(pre_screen, self.speed, self.camera_coordinates)
            self.level_end.render(pre_screen, self.camera_coordinates)
        if self.is_menu:
            self.menu.render(pre_screen)
        if self.paused:
            self.pause.render(pre_screen)
        if self.passed:
            text = f.render("УРОВЕНЬ ПРОЙДЕН", True, (0, 200, 0))
            text1 = f.render("НАЖМИТЕ ЛЮБУЮ КНОПКУ", True, (0, 200, 0))
            rect = text.get_rect(center=(self.info.current_w // 2, self.info.current_h // 2))
            rect1 = text1.get_rect(center=(self.info.current_w // 2, self.info.current_h // 2 + 150))
            pre_screen.blit(text, rect)
            pre_screen.blit(text1, rect1)
        if self.special_info:
            self.render_special_info()

    def check_right(self, speed):
        if len(pg.sprite.spritecollide(self.player.right_border, self.sprites, False)) == 0:
            x = self.player.rect.x // self.cell_size + 2
            self.player.x += speed // (int(self.player.sitting) + 1)
            self.camera_coordinates[0] += speed // (int(self.player.sitting) + 1)
            self.player.change()
            if not len(pg.sprite.spritecollide(self.player.left_border, self.sprites, False)) == 0:
                self.player.x = x * self.cell_size
                self.player.change()

    def check_left(self, speed):
        if len(pg.sprite.spritecollide(self.player.left_border, self.sprites, False)) == 0:
            x = self.player.rect.x // self.cell_size + 1
            self.player.x -= speed // (int(self.player.sitting) + 1)
            self.camera_coordinates[0] -= speed // (int(self.player.sitting) + 1)
            self.player.change()
            if not len(pg.sprite.spritecollide(self.player.left_border, self.sprites, False)) == 0:
                self.player.x = x * self.cell_size - 1 
                self.player.change()

    def all_check(self, code):
        if code == "-1":
            self.paused = False
            self.playing = False
            self.is_menu = True
        elif code == "-2" and not self.is_menu:
            self.paused = not self.paused
            self.playing = not self.playing
        elif code != None:
            self.change_level(code)

    def check(self):
        if self.player.rect.y > 5000:
            self.end = True
            return
        if self.level_end.check(self.player.rect):
            self.passed = True
            self.playing = False
        if len(pg.sprite.spritecollide(self.player.down_border, self.sprites, False)) == 0 or self.player.flying:
            self.player.flying = True
            self.player.check_acc()
            self.player.y += round(self.player.acceleration)
            self.camera_coordinates[1] += round(self.player.acceleration)
            self.player.change()
            if not len(pg.sprite.spritecollide(self.player.down_border, self.sprites, False)) == 0:
                self.player.flying = False
                self.player.check_acc()
                self.camera_coordinates[1] += (self.player.rect.bottomright[1] //
                                               self.cell_size - 2) * self.cell_size - self.player.rect.y
                self.player.y = (self.player.rect.bottomright[1] // self.cell_size - 2) * self.cell_size
                self.player.change()
        if not len(pg.sprite.spritecollide(self.player.up_border, self.sprites, False)) == 0:
            self.player.acceleration = 0
            self.player.check_acc()
        self.coordinates_player = self.player.get_coord()

    def jump(self):
        if not len(pg.sprite.spritecollide(self.player.down_border, self.sprites, False)) == 0 and\
                len(pg.sprite.spritecollide(self.player.up_border, self.sprites, False)) == 0:
            self.player.acceleration = -16
            self.player.flying = True
            self.camera_coordinates[1] -= 1
            self.player.y -= 1
            self.check()

    def sit(self):
        if not self.player.sitting:
            if not self.player.flying:
                self.player.sitting = True
        elif len(pg.sprite.spritecollide(self.player.up_border, self.sprites, False)) == 0:
            self.player.sitting = False

    def respawn(self):
        self.coordinates_player = self.respawn_coordinates
        self.camera_coordinates = self.camera_respawn.copy()
        self.player.x = self.respawn_coordinates[0]
        self.player.y = self.respawn_coordinates[1]
        self.end = False
        self.player.change()
        self.check()

    def make_spawn(self):
        if not self.player.flying and not self.player.walking:
            self.camera_respawn = self.camera_coordinates.copy()
            self.respawn_coordinates = [self.coordinates_player[0], self.coordinates_player[1]]

    def render_special_info(self):
        text2 = f.render("XY:" + str(game.player.rect.x) + ", " + str(game.player.rect.y), True, (0, 200, 0))
        text3 = f.render("camXY:" + str(game.camera_coordinates[0]) + ", " + str(game.camera_coordinates[1]), True,
                         (0, 200, 0))
        text4 = f.render('ACC:' + str(game.player.acceleration), True, (0, 200, 0))
        rect = text2.get_rect(topleft=(11, 35))
        rect1 = text3.get_rect(topleft=(11, 60))
        rect2 = text4.get_rect(topleft=(11, 85))
        pg.draw.rect(screen, '#808080', rect)
        pg.draw.rect(screen, '#808080', rect1)
        pg.draw.rect(screen, '#808080', rect2)
        screen.blit(text2, rect)
        screen.blit(text3, rect1)
        screen.blit(text4, rect2)
        text = f.render('FLYING:' + str(game.player.flying), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 110))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)
        text = f.render('WALKING:' + str(game.player.walking), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 135))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)
        text = f.render('SITTING:' + str(game.player.sitting), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 160))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)
        text = f.render('PLAYING:' + str(game.playing), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 185))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)
        text = f.render('PAUSED:' + str(game.paused), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 210))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)
        text = f.render('ISMENU:' + str(game.is_menu), True, (0, 200, 0))
        rect = text.get_rect(topleft=(11, 235))
        pg.draw.rect(screen, '#808080', rect)
        screen.blit(text, rect)


pg.init()
screen = pg.display.set_mode((0, 0), pg.RESIZABLE)
clock = pg.time.Clock()
while True:
    game = Game()
    moving = False
    f = pg.font.Font(None, 32)
    while True:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
            elif i.type == pg.KEYDOWN:
                if game.passed:
                    game.passed = False
                    game.is_menu = True 
                moving = True
                if pg.K_F3 == i.key:
                    game.special_info = not game.special_info
                if pg.K_ESCAPE == i.key and not game.is_menu and (game.playing or game.paused):
                    game.all_check("-2")
                if not game.end and game.playing:
                    if pg.K_SPACE == i.key:
                        game.jump()
                        game.player.change()
                    if pg.K_DOWN == i.key:
                        game.sit()
                        game.player.change()
                    if pg.K_r == i.key:
                        game.make_spawn()
            elif i.type == pg.MOUSEBUTTONDOWN:
                if game.is_menu:
                    game.all_check(game.menu.get_level(i.pos))
                if game.paused:
                    game.all_check(game.pause.check(i.pos))
        if moving and not game.end and game.playing:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                if keys[pg.K_LSHIFT]:
                    game.speed = 0.25
                    speed = 10
                elif keys[pg.K_LALT]:
                    game.speed = 0.0625
                    speed = 2
                else:
                    game.speed = 0.125
                    speed = 4
                if keys[pg.K_RIGHT]:
                    game.check_right(speed)
                    game.player.side = "R"
                else:
                    game.check_left(speed)
                    game.player.side = "L"
                game.player.walking = True
            else:
                game.player.walking = False
            if keys[pg.K_UP]:
                game.jump()
                game.player.change()
            if keys[pg.K_a]:
                game.camera_coordinates[0] -= 30
            if keys[pg.K_w]:
                game.camera_coordinates[1] -= 30
            if keys[pg.K_d]:
                game.camera_coordinates[0] += 30
            if keys[pg.K_s]:
                game.camera_coordinates[1] += 30
                print('wret')
            if keys[pg.K_q]:
                print("123")
                break
            if keys[pg.K_e]:
                game.respawn()
        screen.fill('#d0d0d0')
        game.render(screen)
        if game.playing:
            game.check()
            text1 = f.render(str(round(clock.get_fps()) + 10000) + " FPS", True, (0, 200, 0))
            rect = text1.get_rect(topleft=(11, 11))
            pg.draw.rect(screen, '#808080', rect)
            screen.blit(text1, rect)
        pg.display.update()
        if game.end:
            game.respawn()
        clock.tick(60)
