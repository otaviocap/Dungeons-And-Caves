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
            self.game.player.life -= 2
            for i in self.game.enemies.sprites():
                i.resetLocation()
        for i in self.game.enemies.sprites():
            if pygame.sprite.collide_rect(self, i):
                # i.resetLocation()
                i.kill()