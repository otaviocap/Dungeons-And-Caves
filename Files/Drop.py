import pygame
from textEngine import textGui
from random import randint

class Drop(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w=16, h=16, forceItem=None):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.game = game
        self.spawnX = x
        self.spawnY = y
        self.image = pygame.image.load('../Assets/Drops.png')
        self.getItems()
        if forceItem is None:
            self.dropStrenght = randint(0, 3)

        else:
            self.dropStrenght = forceItem

        self.dropColor = randint(4, 7)
        self.itemImg = self.drops[self.dropStrenght]
        self.dropImg = self.drops[self.dropColor]
        self.itemRect = self.itemImg.get_rect()
        self.dropRect = self.dropImg.get_rect()
        self.textGui = textGui()
        self.game.allDrops.add(self)
        self.makeText()
        self.itemRect.x = self.x
        self.itemRect.y = self.y
        self.dropRect.x = self.x
        self.dropRect.y = self.y
        self.rect = self.dropRect
        self.actionDone = False
        self.collided = False

    def getItems(self):
        self.drops = []
        pos = [-16, 0]
        for i in range(12):
            if pos[0] == 48:
                pos[0] = 0
                pos[1] += 16
            else:
                pos[0] += 16
            self.drops.append(self.image.subsurface(pos, (16, 16)))

    def makeText(self):
        self.text = 'Life UP:\n'
        if self.dropStrenght == 0:
            self.text += '+1'
        elif self.dropStrenght == 1:
            self.text += '+3'
        elif self.dropStrenght == 2:
            self.text += '+4'
        elif self.dropStrenght == 3:
            self.text += '+5'

    def update(self):
        nText = 0
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.dropImg = self.drops[self.dropColor + 4]
            text = ''
            textPos = 10
            for character in self.text:
                if character == "\n":
                    self.game.texts['Drop' + str(nText)] = (text, (self.x, self.y + textPos))
                    text = ''
                    nText += 1
                    textPos += 10
                else:
                    text += character
            self.game.texts['Drop'] = (text, (self.x, self.y + textPos))
            self.collided = True
        if self.collided:
            if self.itemRect.y - self.spawnY > -30:
                self.itemRect.y -= .5
            else:
                for i in range(nText):
                    self.game.texts.pop('Drop' + str(i))
                self.game.texts.pop('Drop')
                self.game.texts.clear()
                self.kill()
            self.itemAction()

    def itemAction(self):
        if not self.actionDone:
            self.actionDone = True
            item = self.dropStrenght
            if item == 0:
                for player in self.game.players.sprites():
                    player.life += 1

            elif item == 1:
                for player in self.game.players.sprites():
                    player.life += 3

            elif item == 2:
                for player in self.game.players.sprites():
                    player.life += 4

            elif item == 3:
                for player in self.game.players.sprites():
                    player.life += 5

    def draw(self):
        self.game.screen.blit(self.itemImg, self.game.camera.apply_rect(self.itemRect))
        self.game.screen.blit(self.dropImg, self.game.camera.apply(self))

