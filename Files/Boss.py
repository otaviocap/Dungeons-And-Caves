import pygame
from Enemy import *

class Boss(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.life = 100
        self.live = False
        self.wave = 0
        self.copies = pygame.sprite.Group()
        self.copiesRespawn = []
        self.changedPos = False
        self.enemies = []

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def addCopy(self, x, y):
        self.copies.add(bossCopy(self.game, x, y))
        self.copiesRespawn.append([x, y])

    def addEnemiesArena(self, x, y, width, height):
        self.enemies.append([x, y, width, height])

    def draw(self):
        for i in self.copies.sprites():
            i.draw()

    def update(self):
        self.copies.update()
        if len(self.copies.sprites()) == 0 and not self.changedPos:
            self.game.player.setPos(self.spawn1[0], self.spawn1[1])
            for i in self.enemies:
                Enemy(self.game, i[0], i[1], 16, 16)
            self.changedPos = True
            self.wave += 1
        if len(self.game.enemies.sprites()) == 0 and self.changedPos:
            self.game.player.setPos(self.spawn[0], self.spawn[1])
            self.spawnCopies()
            self.changedPos = False

    def setSpawn(self, x, y):
        self.spawn = [x, y]

    def setSpawn1(self, x, y):
        self.spawn1 = [x, y]

    def setSpawn2(self, x, y):
        self.spawn2 = [x, y]

    def spawnCopies(self):
        for i in self.copiesRespawn:
            self.copies.add(bossCopy(self.game, i[0], i[1]))

class bossCopy(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.life = 10
        self.img = pygame.image.load('../Assets/bossCopy.png')
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        self.game.screen.blit(self.img, self.game.camera.apply(self))

    def update(self):
        for i in self.game.bullets.sprites():
            if pygame.sprite.collide_rect(self, i):
                i.kill()
                self.kill()



