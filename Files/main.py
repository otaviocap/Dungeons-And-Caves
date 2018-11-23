import pygame
from Player import *
from Bullet import *
from Interpreter import *
from Map import *
from Camera import *
from Hud import *
from End import *
from Hole import *
from Spike import *
from Enemy import *


class game():

    def __init__(self):
        #Variaveis iniciais

        pygame.init()
        self.eventDamage = pygame.USEREVENT + 1
        self.tempVar = 0
        self.data = Interpreter('configs')
        self.speedB = 5
        self.velocity = 1
        self.screenSize = self.data.getParameter('screenSize')
        self.fps = self.data.getParameter('fps')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.screen.set_alpha(128)
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.done = False
        self.mag = 10
        self.debugStatus = self.data.getParameter('debug')
        self.mapsAlreadyPlayed = ['../Maps\\map1.tmx']
        print(self.debugStatus)

    def new(self, mapPath = '../Maps/map4.tmx'):

        self.mapPath = mapPath
        self.map = tiledMap(mapPath)
        self.mapImg = self.map.makeMap(self)
        self.mapRect = self.mapImg.get_rect()
        self.camera = Camera(self.mapRect.x, self.mapRect.y)


        self.frontSprites = pygame.sprite.Group()
        self.backSprites = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemyBullet = pygame.sprite.Group()

        for i in self.map.tmdata.objects:
            if i.name == 'spawn':
                self.player = Player(self, i.x, i.y)
            elif i.name == 'wall':
                Wall(self, i.x, i.y, i.width, i.height)
            elif i.name == 'end':
                End(self, i.x, i.y, i.width, i.height)
            elif i.name == 'hole':
                Hole(self, i.x, i.y, i.width, i.height)
            elif i.name == 'spike' and i.type == 'on':
                Spike(self, i.x, i.y, i.width, i.height)
            elif i.name == 'enemy':
                Enemy(self, i.x, i.y, i.width, i.height)


        self.hud = Hud(self)
        self.camera = Camera(self.mapRect.width, self.mapRect.height)
        print(self.walls)
        print(self.triggers)
        print(self.mapsAlreadyPlayed)

    def gameRun(self):
        self.new()
        while not self.done:
            self.events()
            self.update()
            self.debug()
            self.draw()
        pygame.quit()


    def events(self):
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_0:
                self.player.life += 1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_9:
                self.player.life -= 1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_8:
                self.player.maxLife += 2
                self.tempVar += 1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_7:
                self.player.maxLife -= 2
                self.tempVar -= 1
            elif e.type == self.eventDamage:
                self.player.life -= 1



        if self.player.checkCooldownHab1():
                if key[pygame.K_LEFT]:
                    Bullet('left', self.speedB, self, self.player)
                    self.player.setDirection('left')
                    self.player.setCooldown(self.player.hab1cooldown)
                elif key[pygame.K_RIGHT]:
                    Bullet('right', self.speedB, self, self.player)
                    self.player.setDirection('right')
                    self.player.setCooldown(self.player.hab1cooldown)
                elif key[pygame.K_UP]:
                    Bullet('up', self.speedB, self, self.player)
                    self.player.setCooldown(self.player.hab1cooldown)
                elif key[pygame.K_DOWN]:
                    Bullet('down', self.speedB, self, self.player)
                    self.player.setCooldown(self.player.hab1cooldown)

    def update(self):
        self.clock.tick(self.fps)
        self.velocity = 2
        self.camera.update(self.player)
        self.allSprites.update()
        self.triggers.update()
        self.holes.update()
        self.spikes.update()
        self.enemies.update()
        pygame.display.set_caption(str(self.player.getPos()) + 'FPS = ' + str(self.clock.get_fps()))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map.underLayer, self.camera.apply_rect(self.mapRect))
        for i in self.enemies:
            self.screen.blit(i.enemiesTypes[i.enemyType], self.camera.apply(i))
        for i in self.allSprites.sprites():
            self.screen.blit(i.getImg(), self.camera.apply(i))
        self.screen.blit(self.map.upperLayer, self.camera.apply_rect(self.mapRect))
        self.hud.draw()
        pygame.display.flip()

    def debug(self):
        if self.debugStatus:
            temp = pygame.Surface((self.player.rect.width, self.player.rect.height))
            temp.fill((255, 255, 255))
            self.screen.blit(temp, self.camera.apply(self.player))



if __name__ == '__main__':
    a = game()
    a.gameRun()
