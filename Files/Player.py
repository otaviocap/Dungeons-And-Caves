import pygame



class Player(pygame.sprite.Sprite):
    def __init__(self, game, n, x=0, y=0, sizeX=10, sizeY=10):
        super().__init__()
        self.dashM = 50
        self.direction = 'left'
        self.game = game
        self.game.allSprites.add(self)
        self.hab1cooldown = 30
        self.game.players.add(self)
        self.life = 4
        self.maxLife = 8
        self.image = pygame.image.load('../Assets/character'+str(n)+'.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], self.image.get_size()[1]))
        self.rect = pygame.Rect(x, y, self.image.get_rect().width, self.image.get_rect().height)
        self.cooldown = 0
        # self.original = pygame.image.load('../Assets/character.gif')
        # self.original = pygame.transform.scale(self.original, (self.getSize()[0] ** 2, self.getSize()[1] ** 2))
        self.transformImgSide()
        self.gunBarrel = [100, 100]
        self.velocity = 2
        self.x = x
        self.y = y
        self.spawnX = x
        self.spawnY = y
        self.w = sizeX
        self.h = sizeY
        self.damage = 1
        self.speed = 1
        self.useSpeed = 1
        self.defense = 0
        self.magicBook = 0
        # self.gunBarrel = [X , Y]

    def update(self):
        self.goCooldownHab1()
        self.move()
        if self.life >= self.maxLife:
            self.life = self.maxLife
        if self.life <= 0:
            self.life = 0
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
        self.cooldown = n

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

    def dash(self):
        if self.direction == "down":
            self.y += self.dashM
        elif self.direction == "up":
            self.y -= self.dashM
        elif self.direction == "left":
            self.x -= self.dashM
        elif self.direction == "right":
            self.x += self.dashM

    def hit(self):
        if pygame.sprite.spritecollide(self, self.game.enemyBullet, False):
            self.life -= self.game.enemyBullet.sprites()[0].damage

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
