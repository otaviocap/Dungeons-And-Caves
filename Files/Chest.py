import pygame
from random import choice
from Enemy import Enemy
from Upgrades import Upgrade

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
        self.chestChoosen = 2#choice([0,2,4])
        self.image = self.chestStates[self.chestChoosen]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.spawned = False


    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.openChest()

    def openChest(self):
        if self.chestChoosen == 0 and not self.spawned:
            self.image = self.chestStates[self.chestChoosen + 1]
            self.spawned = True

        elif self.chestChoosen == 2 and not self.spawned:
            self.image = self.chestStates[self.chestChoosen + 1]
            Upgrade(self.game, self.x, self.y)
            self.spawned = True

        elif self.chestChoosen == 4 and not self.spawned:
            self.image = self.chestStates[self.chestChoosen + 1]
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



