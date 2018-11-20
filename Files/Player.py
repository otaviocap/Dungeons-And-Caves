import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0, sizeX=10, sizeY=10):
        super().__init__()
        self.direction = 'right'
        self.size = (sizeX, sizeY)
        self.game = game
        self.image = pygame.image.load('../Assets/character2.png')
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
        self.w = sizeX
        self.h = sizeY
        # self.gunBarrel = [X , Y]

    def update(self):
        self.move()
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collideWall('x')
        self.rect.y = self.y
        self.collideWall('y')


    def move(self):
        self.vx, self.vy, self.velocity = 0, 0, 2

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            self.velocity = 3
        elif key[pygame.K_LCTRL]:
            self.velocity = 1
        if key[pygame.K_a]:
            self.vx = -self.velocity
        if key[pygame.K_d]:
            self.vx = self.velocity
        if key[pygame.K_w]:
            self.vy = -self.velocity
        if key[pygame.K_s]:
            self.vy = self.velocity

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

    def checkCooldown(self):
        if self.cooldown == 0:
            return True

    def setCooldown(self, n):
        self.cooldown = n

    def getCooldown(self):
        return self.cooldown

    def goCooldown(self):
        if self.cooldown == 0:
            pass
        else:
            self.cooldown -= 1

    def getSize(self):
        return self.size

    def setSize(self, size, screen):
        self.size += size
        pygame.transform.scale(screen, self.size)

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
