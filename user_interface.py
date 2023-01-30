import button
import sys


class Pause:
    def __init__(self):
        self.message = button.Button("data/button.png", 0, 0, "CONTINUE")
        self.to_menu = button.Button("data/button.png", 0, 150, "MENU")
        self.exit = button.Button("data/button.png", 0, 300, "EXIT")

    def check(self, pos):
        if self.message.rect.collidepoint(pos):
            return "-2"
        if self.to_menu.rect.collidepoint(pos):
            return "-1"
        if self.exit.rect.collidepoint(pos):
            sys.exit()
            # BYE :)

    def render(self, screen_):
        self.message.render(screen_)
        self.to_menu.render(screen_)
        self.exit.render(screen_)


class Menu:
    def __init__(self, *levels):
        self.levels = list(levels[0])
        self.levels.append("EXIT")
        self.buttons = []
        for i in range(len(self.levels)):
            self.buttons.append(button.Button("data/button.png", i // 5 * 250, i % 5 * 150, self.levels[i]))

    def render(self, screen_):
        for i in self.buttons:
            i.render(screen_)

    def get_level(self, pos):
        for i in self.buttons:
            if i.clicked(pos):
                if i.message == "EXIT":
                    sys.exit()
                    # BYE :)
                if i.message == "START":
                    return "0"
                return i.message
