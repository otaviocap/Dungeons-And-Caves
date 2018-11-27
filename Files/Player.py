import pygame
from Upgrades import Upgrade



class Player(pygame.sprite.Sprite):
    def __init__(self, game, n, x=0, y=0, sizeX=10, sizeY=10):
        super().__init__()
        self.direction = 'left'
        self.game = game
        self.flying = True
        self.inverseKnockback = False
        self.game.allSprites.add(self)
        self.saves = self.game.saves
        self.hab1cooldown = self.game.saves.playerA1['cooldown']
        self.game.players.add(self)
        self.life = self.game.saves.playerA1['life']
        self.maxLife = self.game.saves.playerA1['maxLife']
        self.image = pygame.image.load('../Assets/character'+str(n)+'.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], self.image.get_size()[1]))
        self.rect = pygame.Rect(x, y, self.image.get_rect().width, self.image.get_rect().height)
        self.cooldown = 0
        # self.original = pygame.image.load('../Assets/character.gif')
        # self.original = pygame.transform.scale(self.original, (self.getSize()[0] ** 2, self.getSize()[1] ** 2))
        self.transformImgSide()
        self.gunBarrel = [100, 100]
        self.x = x
        self.y = y
        self.spawnX = x
        self.spawnY = y
        self.w = sizeX
        self.h = sizeY
        self.damage = self.game.saves.playerA1['damage']
        self.speed = self.game.saves.playerA1['speed']
        self.useSpeed = 1
        self.defense = self.game.saves.playerA1['defense']
        self.magicBook = self.game.saves.playerA1['magicBook']
        self.action = False
        self.setMagic(self.magicBook)
        # self.gunBarrel = [X , Y]

    def update(self):
        self.goCooldownHab1()
        self.magicEffect()
        self.move()
        if self.life >= self.maxLife:
            self.life = self.maxLife
        if self.life <= 0:
            self.life = 0
        if self.hab1cooldown <= 5:
            self.hab1cooldown = 5
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collideWall('x')
        self.rect.y = self.y
        self.collideWall('y')
        self.hit()
        self.game.life = self.life

    def move(self):
        self.useSpeed = self.speed
        self.vx, self.vy = 0, 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            self.useSpeed = self.useSpeed + 1
        elif key[pygame.K_LCTRL]:
            self.useSpeed = 1
        elif key[pygame.K_e]:
            self.action = True
        if key[pygame.K_a]:
            self.vx = -self.useSpeed
        if key[pygame.K_d]:
            self.vx = self.useSpeed
        if key[pygame.K_w]:
            self.vy = -self.useSpeed
        if key[pygame.K_s]:
            self.vy = self.useSpeed

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

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

    def changeSpawn(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def checkCooldownHab1(self):
        if self.cooldown == 0:
            return True

    def setCooldown(self, n):
        self.cooldown = self.hab1cooldown

    def getCooldownHab1(self):
        return self.cooldown

    def goCooldownHab1(self):
        if self.cooldown == 0:
            pass
        else:
            self.cooldown -= 1

    def getImg(self):
        return self.image

    def transformImgSide(self):
        # self.image = self.original
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)

    def setDirection(self, direction):
        if not self.direction == direction:
            self.direction = direction
            self.transformImgSide()

    def setPos(self, x, y):
        self.spawnY = y
        self.spawnX = x
        self.x = x
        self.y = y

    def resetLocation(self):
        self.x = self.spawnX
        self.y = self.spawnY

    def hit(self):
        if pygame.sprite.spritecollide(self, self.game.enemyBullet, False):
            self.life -= self.game.enemyBullet.sprites()[0].damage

    def setMagic(self, n):
        self.bookMagicCooldown = self.game.saves.playerA1['magicCooldown']
        self.effectTime = 0
        if n == 0:
            self.bookImg = pygame.image.load('../Assets/originalBook.png')
            self.magic = 0
            self.bookMagicCooldownDefault = 0
            self.effectTimeDefault = 0
        elif n == 1:
            self.bookImg = Upgrade(self.game, 0, 0).items[0]
            self.magic = 1
            self.bookMagicCooldownDefault = 5
            self.effectTimeDefault = 0
        elif n == 2:
            self.bookImg = Upgrade(self.game, 0, 0).items[1]
            self.magic = 2
            self.bookMagicCooldownDefault = 30 * 60
            self.effectTimeDefault = 5 * 60
        elif n == 3:
            self.bookImg = Upgrade(self.game, 0, 0).items[2]
            self.magic = 3
            self.bookMagicCooldownDefault = 25 * 60
            self.effectTimeDefault = 0
        elif n == 4:
            self.bookImg = Upgrade(self.game, 0, 0).items[3]
            self.magic = 4
            self.bookMagicCooldownDefault = 45 * 60
            self.effectTimeDefault = 0
        elif n == 5:
            self.bookImg = Upgrade(self.game, 0, 0).items[4]
            self.magic = 5
            self.bookMagicCooldownDefault = 30 * 60
            self.effectTimeDefault = 10 * 60
        self.backToNormal = self.game.saves.playerA1['magicCooldown']

    def magicEffect(self):
        if self.bookMagicCooldown <= 0 and self.game.action:
            if self.magic == 0:
                pass

            elif self.magic == 1:
                self.flying = not self.flying
                self.bookMagicCooldown = self.bookMagicCooldownDefault
                self.effectTime = self.effectTimeDefault

            elif self.magic == 2:
                self.damage = self.damage * 2
                self.bookMagicCooldown = self.bookMagicCooldownDefault
                self.effectTime = self.effectTimeDefault

            elif self.magic == 3:
                self.inverseKnockback = not self.inverseKnockback
                self.bookMagicCooldown = self.bookMagicCooldownDefault
                self.effectTime = self.effectTimeDefault

            elif self.magic == 4:
                for i in self.game.enemies.sprites():
                    i.life -= 2
                self.bookMagicCooldown = self.bookMagicCooldownDefault
                self.effectTime = self.effectTimeDefault

            elif self.magic == 5:
                self.damage += 2
                self.life -= 2
                self.bookMagicCooldown = self.bookMagicCooldownDefault
                self.effectTime = self.effectTimeDefault
            self.game.action = False
            self.backToNormal = False
        else:
            if self.bookMagicCooldown <= 0:
                self.bookMagicCooldown = 0
            else:
                self.bookMagicCooldown -= 1

            if self.effectTime <= 0:
                self.effectTime = 0
                if not self.backToNormal:
                    if self.magic == 2:
                        self.damage = self.damage / 2
                        self.backToNormal = True
                    elif self.magic == 5:
                        self.damage -= 2
                        self.backToNormal = True
            else:
                self.effectTime -= 1
            print('Cooldown = ', self.bookMagicCooldown)
            print('EffectTime = ', self.effectTime)










class Wall(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        game.walls.add(self)
        self.game = game
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
