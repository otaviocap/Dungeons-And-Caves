import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, direction, speed, game, where, enemyBullet=False, damage=1):
        super().__init__()
        self.game = game
        self.game.allSprites.add(self)
        self.direction = direction
        self.size = (10, 10)
        self.screenSize = self.game.screenSize
        self.color = (0, 255, 0)
        self.image = pygame.image.load('../Assets/magic.png')
        self.image = pygame.transform.scale(self.image, self.size)
        self.transformImgSide()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = direction
        self.rect.x = where.x
        self.rect.y = where.y
        self.starTime = pygame.time.get_ticks()
        self.damage = damage
        self.enemyBullet = enemyBullet
        if enemyBullet:
            self.game.enemyBullet.add(self)
        else:
            self.game.bullets.add(self)

    def update(self):
        if (pygame.time.get_ticks() - self.starTime) >= 30:
            if pygame.sprite.spritecollide(self, self.game.walls, False) or (pygame.time.get_ticks() - self.starTime) >= 1000:
                self.kill()
        if (pygame.time.get_ticks() - self.starTime) >= 30 and self.enemyBullet:
            if pygame.sprite.spritecollide(self, self.game.players, False) or (pygame.time.get_ticks() - self.starTime) >= 1000:
                self.kill()
        if self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

    def getColor(self):
        return self.color

    def getSize(self):
        if self.direction == "down":
            return (self.size[0], self.size[1])
        elif self.direction == "up":
            return (self.size[0], self.size[1])
        elif self.direction == "left":
            return (self.size[1], self.size[0])
        elif self.direction == "right":
            return (self.size[1], self.size[0])

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def getImg(self):
        return self.image

    def transformImgSide(self):
        if self.direction == "down":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "up":
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == "left":
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.direction == "right":
            self.image = pygame.transform.rotate(self.image, 180)

