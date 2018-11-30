from random import randint
from Bullet import *
from Drop import Drop

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h, forceEnemy=None, str=None, speed=1, life=3):
        super().__init__()
        self.game = game
        self.speedDefault = speed
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.life = life
        self.spawnX = x
        self.spawnY = y
        self.enemiesImg = pygame.image.load('../Assets/Enemies.png')
        self.getEnemiesImg()
        self.timeSinceLastDmg = 0
        if forceEnemy is None:
            self.enemyType = randint(0, len(self.enemiesTypes) -1)
            self.rect = self.enemiesTypes[self.enemyType].get_rect()
        elif isinstance(forceEnemy, pygame.Surface):
            self.enemiesTypes.append(forceEnemy)
            self.enemyType = -1
            self.rect = self.enemiesTypes[self.enemyType].get_rect()
            self.life = 6
        else:
            self.enemiesTypes.append(pygame.image.load(forceEnemy))
            self.enemyType = -1
            self.rect = self.enemiesTypes[self.enemyType].get_rect()
        if str != None:
            self.strength = str
        else:
            if self.enemyType <= 3:
                self.strength = self.enemyType
            else:
                self.strength = 1
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.enemies.add(self)
        self.clock = pygame.time.Clock()
        self.cooldown = 60
        self.time = 0

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

    def collideHoles(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.holes, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.holes, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def move(self):
        self.vx, self.vy, self.speed = 0, 0, self.speedDefault
        self.x = self.rect.x
        self.y = self.rect.y
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -= self.speed
            self.collideWall('x')
            self.collideHoles('x')
            self.collideEnemy('x')
        elif self.rect.x < self.game.player.rect.x:
            self.rect.x += self.speed
            self.collideWall('x')
            self.collideHoles('x')
            self.collideEnemy('x')
        if self.rect.y < self.game.player.rect.y:
            self.rect.y += self.speed
            self.collideWall('y')
            self.collideHoles('y')
            self.collideEnemy('y')
        elif self.rect.y > self.game.player.rect.y:
            self.rect.y -= self.speed
            self.collideWall('y')
            self.collideHoles('y')
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
            self.timeSinceLastDmg += self.time
            damage = self.strength - self.game.player.defense
            if damage <= 0:
                damage = 0
            if self.timeSinceLastDmg >= 1000:
                self.game.player.life -= damage
                self.timeSinceLastDmg = 0
        if self.enemyType >= 5 or self.enemyType <= -1:
            if self.checkCooldown():
                if self.rect.x > self.game.player.rect.x:
                    Bullet('left', 3, self.game, self, True)
                    self.cooldown = 60
                elif self.rect.y > self.game.player.rect.y:
                    Bullet('up', 3, self.game, self, True)
                    self.cooldown = 60
                elif self.rect.x < self.game.player.rect.x:
                    Bullet('right', 3, self.game, self, True)
                    self.cooldown = 60
                elif self.rect.y < self.game.player.rect.y:
                    Bullet('down', 3, self.game, self, True)
                    self.cooldown = 60

    def hit(self):
        for i in self.game.bullets.sprites():
            if pygame.sprite.collide_rect(self, i):
                if not self.game.player.inverseKnockback:
                    if i.direction == "down":
                        self.rect.y += 5
                        self.collideWall('y')
                        self.collideEnemy('y')

                    elif i.direction == "up":
                        self.rect.y -= 5
                        self.collideWall('y')
                        self.collideEnemy('y')

                    elif i.direction == "left":
                        self.rect.x -= 5
                        self.collideWall('x')
                        self.collideEnemy('x')

                    elif i.direction == "right":
                        self.rect.x += 5
                        self.collideWall('x')
                        self.collideEnemy('x')
                else:
                    if i.direction == "down":
                        self.rect.y -= 5
                        self.collideWall('y')
                        self.collideEnemy('y')

                    elif i.direction == "up":
                        self.rect.y += 5
                        self.collideWall('y')
                        self.collideEnemy('y')

                    elif i.direction == "left":
                        self.rect.x += 5
                        self.collideWall('x')
                        self.collideEnemy('x')

                    elif i.direction == "right":
                        self.rect.x -= 5
                        self.collideWall('x')
                        self.collideEnemy('x')

                self.life -= self.game.players.sprites()[0].damage
                i.kill()

        self.checkLife()

    def checkLife(self):
        if self.life <= 0:
            if randint(0, 201) % 20 == 0:
                Drop(self.game, self.x, self.y)
            self.kill()
        else:
            pass


    def resetLocation(self):
        self.rect.x = self.spawnX
        self.rect.y = self.spawnY
