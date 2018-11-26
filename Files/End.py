import pygame
from glob import glob
from random import choice
import os

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
        self.maps = [f for f in glob('../Maps/map*.tmx') if not os.path.basename(f).startswith('mapBoss')]
        self.bossMaps = glob('../Maps/mapBoss*.tmx')

    def update(self):
        if len(self.game.enemies.sprites()) <= 0:
            if pygame.sprite.spritecollide(self, self.game.players, False):
                self.game.saves.update(self.game.player1)
                newMap = self.getChoosed()
                self.game.new(newMap)

    def getChoosed(self):
        self.choosed = choice(self.maps)
        if len(self.game.mapsAlreadyPlayed) >= len(self.maps):
            self.game.mapsAlreadyPlayed.clear()
            self.choosed = choice(self.bossMaps)
        else:
            while self.choosed in self.game.mapsAlreadyPlayed:
                self.choosed = choice(self.maps)
        self.game.mapsAlreadyPlayed.append(self.choosed)
        return self.choosed

