import pygame
from textEngine import textGui
from MenuUI import Button
from saveGetter import saveGetter

class Save(pygame.sprite.Sprite):

    def __init__(self, game, menu, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.buttons = []
        self.rect = pygame.rect.Rect(x,y,w,h)
        self.game = game
        self.menu = menu
        self.b = []
        self.texts = {}
        self.game.savers.add(self)
        self.opened = False
        self.screen = self.game.screen
        self.textGui = textGui()
        self.goingDown = 0

    def openMenu(self):
        self.b.append(Button(self, 365, 70, image=[self.menu.images[10], self.menu.images[11]], text='Slot 1', selectable=True))
        self.b.append(Button(self, 365, 155, image=[self.menu.images[10], self.menu.images[11]], text='Slot 2', selectable=True))
        self.b.append(Button(self, 365, 240, image=[self.menu.images[10], self.menu.images[11]], text='Slot 3', selectable=True))
        self.b.append(Button(self, 405, 355, image=[self.menu.images[14], self.menu.images[14]], action='self.menu.saveGame()'))
        self.b.append(Button(self, 405, 355, image=[self.menu.images[14], self.menu.images[14]], action='self.menu.goingDown = 0'))
        self.b.append(Button(self, 405, 355, image=[self.menu.images[14], self.menu.images[14]], action='self.menu.texts["text"] = ["Save Completed", [self.x, self.y]]'))
        self.b.append(Button(self, 405, 355, image=[self.menu.images[14], self.menu.images[14]], action='self.menu.b.clear()'))


    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            if self.game.action and not self.opened:
                if not self.game.player.magicBook == 0:
                    self.game.player.bookMagicCooldown += 10
                self.openMenu()
                self.opened = True
                self.game.player.action = False
        else:
            self.game.action = False
            self.opened = False
            self.b.clear()
        for key, text in self.texts.items():
            text[1][1] -= self.goingDown
            self.goingDown -= .25
            if self.goingDown == -20:
                self.texts.clear()
                break

    def saveGame(self):
        for button in self.b:
            if button.clicked:
                saveGetter(self.game, button.text)

    def draw(self):
        for button in self.b:
            button.update()
            button.draw()
        for key, text in self.texts.items():
            self.screen.blit(self.textGui.text(text[0], color=(255, 255, 255)), text[1])
