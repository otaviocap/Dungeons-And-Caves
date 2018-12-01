import pygame
from Enemy import *
from random import randint
from Sounds import Sound

class BossController(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        Sound().bossMusics[0].play()
        self.game = game
        self.wave = 0
        self.copies = pygame.sprite.Group()
        self.bossGroup = pygame.sprite.Group()
        self.copiesRespawn = []
        self.changedPos = False
        self.alive = False
        self.enemies = []
        self.enemiesAfter = []

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
        if len(self.bossGroup.sprites()) > 0:
            self.boss.draw()


    def update(self):
        self.copies.update()
        if self.wave == 2:
            self.alive = True
            self.game.player.setPos(self.spawn2[0], self.spawn2[1])
            self.boss = Boss(self, self.bossSpawn[0], self.bossSpawn[1])
            self.wave = 0
        elif len(self.copies.sprites()) == 0 and len(self.game.enemies.sprites()) == 0 and not self.changedPos and not self.alive:
            self.game.player.setPos(self.spawn1[0], self.spawn1[1])
            self.changedPos = True
            self.wave += 1
            if self.wave != 2:
                for i in self.enemies:
                    Enemy(self.game, i[0], i[1], 16, 16)
        elif len(self.game.enemies.sprites()) == 0 and self.changedPos and not self.alive:
            self.game.player.setPos(self.spawn[0], self.spawn[1])
            self.spawnCopies()
            if self.wave == 1:
                self.spawnAfterEnemies()
            self.changedPos = False
        if len(self.bossGroup.sprites()) > 0:
            self.boss.update()


    def setSpawn(self, x, y):
        self.spawn = [x, y]

    def setSpawn1(self, x, y):
        self.spawn1 = [x, y]

    def setSpawn2(self, x, y):
        self.spawn2 = [x, y]

    def setBossSpawn(self, x, y):
        self.bossSpawn = [x, y]

    def spawnCopies(self):
        for i in self.copiesRespawn:
            self.copies.add(bossCopy(self.game, i[0], i[1]))

    def spawnAfterEnemies(self):
        for i in self.enemiesAfter:
            self.game.enemies.add(Enemy(self.game, i[0], i[1], 16, 16))

    def addEnemiesAfter(self, x, y):
        self.enemiesAfter.append([x, y])

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
        self.strength = 2
        self.timeSinceLastDmg = 0

    def draw(self):
        self.game.screen.blit(self.img, self.game.camera.apply(self))

    def update(self):
        for i in self.game.bullets.sprites():
            if pygame.sprite.collide_rect(self, i):
                if self.life == 0:
                    self.kill()
                self.life -= self.game.player.damage
                i.kill()
        self.damage()

    def damage(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            self.time = self.damageClock.tick()
            self.timeSinceLastDmg += self.time
            damage = int(self.strength - self.game.player.defense/2)
            if damage <= 0:
                damage = 0
            if self.timeSinceLastDmg >= 1000:
                self.controller.game.player.life -= damage
                self.timeSinceLastDmg = 0

class Boss(pygame.sprite.Sprite):

    def __init__(self, controller, x, y):
        super().__init__()
        self.controller = controller
        self.controller.bossGroup.add(self)
        self.x = x
        self.y = y
        self.life = 500
        self.alive = False
        self.getStates()
        self.state = 9
        self.clock = pygame.time.Clock()
        self.damageClock = pygame.time.Clock()
        self.timeToChange = 0
        self.cooldown = 0
        self.strength = 2
        self.spawning = True
        self.timeSinceLastDmg = 0

    def getStates(self):
        dead = pygame.image.load('../Assets/bossDead.png')
        idle = pygame.image.load('../Assets/bossIdle.png')
        attack = pygame.image.load('../Assets/bossAttack.png')
        self.dead = []
        self.idle = []
        self.attack = []
        self.magic = pygame.image.load('../Assets/bossMagic.png')
        pos = [-31,0]
        for i in range(3):
            pos[0] += 31
            self.idle.append(idle.subsurface(pos, (27, 47)))
        pos = [-64, -64]
        for i in range(2):
            pos[1] += 64
            for j in range(5):
                pos[0] += 64
                self.dead.append(dead.subsurface(pos, (64,64)))
            pos[0] = -64
        pos = [-31, 0]
        for i in range(3):
            pos[0] += 31
            self.attack.append(attack.subsurface(pos, (27, 47)))

    def update(self):

        if self.state >= 0:
            self.time = self.clock.tick()
            self.timeToChange += self.time
            if self.timeToChange >= 300:
                self.timeToChange = 0
                self.state -= 1
            self.renderImg = self.dead[self.state]
        elif self.state >= -3:
            self.spawning = False
            renderState = -self.state - 1
            self.renderImg = self.renderImg = self.idle[self.state]
            self.time = self.clock.tick()
            self.timeToChange += self.time
            if self.timeToChange >= 300:
                self.timeToChange = 0
                self.state -= 1
        else:
            self.state = -1
        self.rect = self.renderImg.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if not self.spawning:
            self.move()
            self.damage()
            self.hit()
        if self.life <= 50:
            self.strength = 4

    def move(self):
        self.speed = randint(0, 4)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x > self.controller.game.player.rect.x:
            self.x -= self.speed
        elif self.x < self.controller.game.player.rect.x:
            self.x += self.speed
        if self.y < self.controller.game.player.rect.y:
            self.y += self.speed
        elif self.y > self.controller.game.player.rect.y:
            self.y -= self.speed

    def damage(self):
        if pygame.sprite.spritecollide(self, self.controller.game.players, False):
            self.time = self.damageClock.tick()
            self.timeSinceLastDmg += self.time
            damage = int(self.strength - self.controller.game.player.defense)
            if damage <= 0:
                damage = 0
            if self.timeSinceLastDmg >= 1000:
                self.controller.game.player.life -= damage
                self.timeSinceLastDmg = 0

        if self.checkCooldown():
            if self.rect.x > self.controller.game.player.rect.x:
                Bullet('left', 5, self.controller.game, self, True, 2, '../Assets/bossMagic.png')
                self.cooldown = 30
            elif self.rect.y > self.controller.game.player.rect.y:
                Bullet('up', 5, self.controller.game, self, True, 2, '../Assets/bossMagic.png')
                self.cooldown = 30
            elif self.rect.x < self.controller.game.player.rect.x:
                Bullet('right', 5, self.controller.game, self, True, 2, '../Assets/bossMagic.png')
                self.cooldown = 30
            elif self.rect.y < self.controller.game.player.rect.y:
                Bullet('down', 5,self.controller.game, self, True, 2, '../Assets/bossMagic.png')
                self.cooldown = 30
        else:
            self.cooldown -= 1

    def draw(self):
        self.controller.game.screen.blit(self.renderImg, self.controller.game.camera.apply(self))


    def checkCooldown(self):
        return self.cooldown == 0

    def hit(self):
        for i in self.controller.game.bullets.sprites():
            if pygame.sprite.collide_rect(self, i):
                self.life -= self.controller.game.players.sprites()[0].damage
                i.kill()

        if self.life <= 0:
            self.kill()




