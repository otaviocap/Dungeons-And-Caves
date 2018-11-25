import pygame
from random import randrange
from Enemy import Enemy

class Chest(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.game = game
        self.game.chests.add(self)
        self.chestImg = pygame.image.load('../Assets/Chests.png')
        self.getStates()
        self.chestChoosen = 4 #randrange(0, 4, 2)
        self.image = self.chestStates[self.chestChoosen]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.spawned = False


    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.openChest()

    def openChest(self):
        self.image = self.chestStates[self.chestChoosen + 1]
        if self.chestChoosen + 1 == 5 and not self.spawned:
            Enemy(self.game, self.x, self.y, self.w, self.h, self.chestStates[5])
            self.spawned = True
            self.kill()

    def getStates(self):
        self.chestStates = []
        pos =[0, -16]
        for i in range(3):
            for j in range(2):
                if j % 2 == 0:
                    pos[1] += 16
                else:
                    pos[0] += 18
                self.chestStates.append(self.chestImg.subsurface(pos, (16, 16)))
            pos[0] = 0



