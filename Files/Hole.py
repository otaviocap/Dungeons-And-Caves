import pygame

class Hole(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.game = game
        self.game.holes.add(self)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.game.player.resetLocation()