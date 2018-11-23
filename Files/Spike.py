import pygame

class Spike(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.game.spikes.add(self)
        self.clock = pygame.time.Clock()
        self.time = 0

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.time = self.clock.tick()
            if self.time > 20:
                    self.game.player.life -= 1
                    self.clock.tick()
        for i in self.game.enemies.sprites():
            if pygame.sprite.collide_rect(self, i):
                self.timeEnemy = self.clock.tick()
                if self.timeEnemy > 20:
                    i.life -= 1
                    self.clock.tick()
