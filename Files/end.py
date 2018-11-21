import pygame
from glob import glob
from random import choice

class End(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.game = game
        self.game.triggers.add(self)
        self.rect = pygame.Rect(x, y, self.w, self.h)

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            newMap = self.getChoosed()
            self.game.new(newMap)

    def getChoosed(self):
        self.maps = glob('../Maps/*.tmx')
        self.choosed = choice(self.maps)
        if self.game.mapsAlreadyPlayed == self.maps:
            self.game.mapsAlreadyPlayed.clear()
        else:
            while self.choosed in self.game.mapsAlreadyPlayed:
                self.choosed = choice(self.maps)
            self.game.mapsAlreadyPlayed.append(self.choosed)
        return self.choosed

