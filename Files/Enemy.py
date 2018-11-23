import pygame
from random import randint
from Bullet import *

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.game = game
        self.enemiesImg = pygame.image.load('../Assets/Enemies.png')
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.spawnX = x
        self.spawnY = y
        self.getEnemiesImg()
        self.enemyType = randint(0, len(self.enemiesTypes) -1)
        self.rect = self.enemiesTypes[self.enemyType].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.enemies.add(self)
        self.clock = pygame.time.Clock()
        self.cooldown = 60
        self.time = 0
        self.life = 3

    def getEnemiesImg(self):
        self.enemiesTypes = []
        pos = [0, 0]
        for i in range(2):
            for x in range(5):
                self.enemiesTypes.append(self.enemiesImg.subsurface((pos[0], pos[1], 13, 16)))
                if x == 0:
                    pos[0] += 16
                elif x == 2:
                    pos[0] += 16
                else:
                    pos[0] += 15
            pos[0] = 0
            pos[1] = 16

    def update(self):
        self.move()
        self.hit()
        self.goCooldown()
        self.damage()


    def collideWall(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collideEnemy(self, dir):
        withoutme = self.game.enemies.copy()
        withoutme.remove(self)
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, withoutme, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, withoutme, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def move(self):
        self.vx, self.vy, self.speed = 0, 0, 1
        self.x = self.rect.x
        self.y = self.rect.y
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -= self.speed
            self.collideWall('x')
            self.collideEnemy('x')
        elif self.rect.x < self.game.player.rect.x:
            self.rect.x += self.speed
            self.collideWall('x')
            self.collideEnemy('x')
        if self.rect.y < self.game.player.rect.y:
            self.rect.y += self.speed
            self.collideWall('y')
            self.collideEnemy('y')
        elif self.rect.y > self.game.player.rect.y:
            self.rect.y -= self.speed
            self.collideWall('y')
            self.collideEnemy('y')

    def checkCooldown(self):
        if self.cooldown == 0:
            return True
        return False

    def goCooldown(self):
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def damage(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.time = self.clock.tick()
            if self.time > 17:
                self.game.player.life -= 1
                self.clock.tick()
        if self.enemyType >= 4:
            if self.checkCooldown():
                if self.rect.x > self.game.player.rect.x:
                    Bullet('left', 3, self.game, self, True)
                    self.cooldown = 60
                elif self.rect.x < self.game.player.rect.x:
                    Bullet('right', 3, self.game, self, True)
                    self.cooldown = 60
                elif self.rect.y < self.game.player.rect.y:
                    Bullet('down', 3, self.game, self, True)
                    self.cooldown = 60

                elif self.rect.y > self.game.player.rect.y:
                    Bullet('up', 3, self.game, self, True)
                    self.cooldown = 60
    def hit(self):
        for i in self.game.bullets.sprites():
            if pygame.sprite.collide_rect(self, i):
                i.kill()
                self.life -= 1
        self.checkLife()

    def checkLife(self):
        if self.life <= 0:
            self.kill()
        else:
            pass


    def resetLocation(self):
        self.rect.x = self.spawnX
        self.rect.y = self.spawnY
