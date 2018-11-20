import pygame
from Player import *
from Bullet import *
from interpreter import *
from map import *
from camera import *


class game():

    def __init__(self):
        #Variaveis iniciais

        pygame.init()
        self.data = interpreter('configs')
        self.hab1cooldown = 10
        self.speedB = 5
        self.velocity = 1
        self.ammo = 45
        self.magCapacity = 10
        self.screenSize = self.data.getParameter('screenSize')
        self.fps = self.data.getParameter('fps')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.screen.set_alpha(128)
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.done = False
        self.map = tiledMap('../Maps/map1.tmx')
        self.frontSprites = pygame.sprite.Group()
        self.backSprites = pygame.sprite.Group()
        self.mapImg = self.map.makeMap(self)
        self.mapRect = self.mapImg.get_rect()
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.camera = Camera(self.mapRect.x, self.mapRect.y)
        self.mag = 10
        self.debugStatus = self.data.getParameter('debug')
        print(self.debugStatus)

    def new(self):
        for i in self.map.tmdata.objects:
            if i.name == 'spawn':
                self.player = Player(self, i.x, i.y)
            if i.name == 'wall':
                Wall(self, i.x, i.y, i.width, i.height)
        self.allSprites.add(self.player)
        self.camera = Camera(self.mapRect.width, self.mapRect.height)
        print(self.walls)

    def gameRun(self):
        self.new()
        while not self.done:
            self.events()
            self.update()
            self.debug()
            self.draw()
        pygame.quit()


    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.done = True
        key = pygame.key.get_pressed()
        if self.player.checkCooldown():
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
                if self.mag == 0:
                    if not self.ammo == 0:
                        self.ammo -= self.magCapacity
                        self.mag = self.magCapacity
                        self.player.setCooldown(50)
                    else:
                        pass
                else:
                    self.mag -= 1
                    if key[pygame.K_LEFT]:
                        Bullet('left', self.speedB, self.screenSize, self)
                        self.player.setDirection('left')
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_RIGHT]:
                        Bullet('right', self.speedB, self.screenSize, self)
                        self.player.setDirection('right')
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_UP]:
                        Bullet('up', self.speedB, self.screenSize, self)
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_DOWN]:
                        Bullet('down', self.speedB, self.screenSize, self)
                        self.player.setCooldown(self.hab1cooldown)

    def update(self):
        self.clock.tick(self.fps)
        self.velocity = 2
        self.camera.update(self.player)
        self.allSprites.update()
        pygame.display.set_caption(str(self.player.getPos()) + 'FPS = ' + str(self.clock.get_fps()))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map.underLayer, self.camera.apply_rect(self.mapRect))
        for i in self.allSprites.sprites():
            self.screen.blit(i.getImg(), self.camera.apply(i))

        self.screen.blit(self.map.upperLayer, self.camera.apply_rect(self.mapRect))
        pygame.display.flip()

    def debug(self):
        if self.debugStatus:
            temp = pygame.Surface((self.player.rect.width, self.player.rect.height))
            temp.fill((255, 255, 255))
            self.screen.blit(temp, self.camera.apply(self.player))



if __name__ == '__main__':
    a = game()
    a.gameRun()
