from Player import *
from os import name
from Map import *
from Camera import *
from Hud import *
from End import *
from Hole import *
from Spike import *
from Enemy import *
from Chest import *
from Upgrades import *
from textEngine import *
from saveGetter import *
from Save import *
from Boss import *

class game():

    def __init__(self, menu):
        #Variaveis iniciais

        pygame.init()
        self.menu = menu
        self.eventDamage = pygame.USEREVENT + 1
        self.resetMusic = pygame.USEREVENT + 2
        self.action = False
        self.tempVar = 0
        self.textGui = textGui()
        self.data = Interpreter('configs')
        self.speedB = 5
        self.screenSize = self.data.getParameter('screenSize')
        self.fps = self.data.getParameter('fps')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.screen.set_alpha(128)
        pygame.display.set_caption("Dungeons And Caves")
        self.clock = pygame.time.Clock()
        self.done = False
        self.mag = 10
        self.debugStatus = self.data.getParameter('debug')
        if name == 'nt':
            self.mapsAlreadyPlayed = ['../Maps\\map1.tmx']
        else:
            self.mapsAlreadyPlayed = ['../Maps/map1.tmx']


    def new(self, mapPath = '../Maps\\map1.tmx'):
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
        self.chests = pygame.sprite.Group()
        self.allUpgrades = pygame.sprite.Group()
        self.allDrops = pygame.sprite.Group()
        self.savers = pygame.sprite.Group()
        self.texts = {}
        self.hasBoss = False
        if name == 'nt':
            if mapPath == '../Maps\\mapBoss1.tmx':
                self.hasBoss = True
        else:
            if mapPath == '../Maps/mapBoss1.tmx':
                self.hasBoss = True
        if self.hasBoss:
            self.boss = BossController(self)

        for i in self.map.tmdata.objects:
            if i.name == 'spawn':
                self.player = Player(self, 1, i.x, i.y)
                if self.hasBoss:
                    self.boss.setSpawn(i.x, i.y)
            elif i.name == 'wall':
                Wall(self, i.x, i.y, i.width, i.height)
            elif i.name == 'end':
                End(self, i.x, i.y, i.width, i.height)
            elif i.name == 'hole':
                Hole(self, i.x, i.y, i.width, i.height)
            elif i.name == 'spike':
                Spike(self, i.x, i.y, i.width, i.height, i.type)
            elif i.name == 'enemy':
                if not self.hasBoss:
                    Enemy(self, i.x, i.y, i.width, i.height)
                else:
                    self.boss.addEnemiesArena(i.x, i.y, i.width, i.height)
            elif i.name == 'chest':
                Chest(self, i.x, i.y, i.width, i.height)
            elif i.name == 'save':
                Save(self, self.menu, i.x, i.y, i.width, i.height)
            elif i.name == 'boss':
                self.boss.setPos(i.x, i.y)
            elif i.name == 'bossCopy':
                self.boss.addCopy(i.x, i.y)
            elif i.name == 'spawn1':
                self.boss.setSpawn1(i.x, i.y)
            elif i.name == 'spawn2':
                self.boss.setSpawn2(i.x, i.y)
            elif i.name == 'bossSpawn':
                self.boss.setBossSpawn(i.x, i.y)
            elif i.name == 'enemyAfter':
                self.boss.addEnemiesAfter(i.x, i.y)


        self.hud = Hud(self)
        self.camera = Camera(self.mapRect.width, self.mapRect.height)
        print(self.walls)
        print(self.triggers)
        print(self.mapsAlreadyPlayed)

    def gameRun(self, loading=None):
        if loading is None:
            self.saveName = 'Slot 0'
            self.saves = saveGetter(self, 'Slot 0')
        else:
            self.saveName = loading
            self.saves = saveGetter(self, loading, loadind=True)
        self.new()
        while not self.done:
            self.events()
            self.update()
            self.debug()
            self.draw()
        self.done = False


    def events(self):
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if len(self.savers.sprites()) > 0:
                    if not self.savers.sprites()[0].opened:
                        self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_0:
                self.player.life += 1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_9:
                self.player.life -= 1
                for i in self.spikes:
                    i.invert()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_8:
                self.player.maxLife += 2
                self.tempVar += 1
                if self.tempVar == 3:
                    self.tempVar = 0
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_7:
                self.player.maxLife -= 2
                self.tempVar -= 1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                for i in self.enemies:
                    i.kill()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_o:
                for i in self.boss.copies:
                    i.kill()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                self.action = True
            elif e.type == self.eventDamage:
                self.player.life -= 1
            elif e.type == self.resetMusic:
                self.menu.sound.playMusic(0,0)
        self.player.events()

    def update(self):
        self.clock.tick(self.fps)
        self.savers.update()
        self.camera.update(self.player)
        self.allSprites.update()
        self.triggers.update()
        self.holes.update()
        self.spikes.update()
        self.enemies.update()
        self.chests.update()
        self.allUpgrades.update()
        self.hud.update()
        self.allDrops.update()
        if self.hasBoss:
            self.boss.update()
        pygame.display.set_caption(str(self.player.getPos()) + 'FPS = ' + str(self.clock.get_fps())) #str(self.player.getPos()) + 'FPS = ' + str(self.clock.get_fps())

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map.underLayer, self.camera.apply_rect(self.mapRect))
        for i in self.spikes:
            self.screen.blit(i.spikeStates[i.getRenderImg()], self.camera.apply(i))
        for i in self.enemies:
            self.screen.blit(i.enemiesTypes[i.enemyType], self.camera.apply(i))
        for i in self.chests:
            self.screen.blit(i.image, self.camera.apply(i))
        for i in self.allSprites.sprites():
            self.screen.blit(i.getImg(), self.camera.apply(i))
        if self.hasBoss:
            self.boss.draw()
        self.screen.blit(self.map.upperLayer, self.camera.apply_rect(self.mapRect))
        for i in self.allUpgrades.sprites():
            self.screen.blit(i.itemImg, self.camera.apply(i))
        for i in self.allDrops.sprites():
            i.draw()
        for i in self.savers.sprites():
            i.draw()
        # if len(self.allDrops.sprites()) != 0:
        # self.screen.blit(Boss(0,0).attack[self.tempVar], (100, 100))
        for key, text in self.texts.items():
            textSurface = self.textGui.text(text[0], color=(255, 255, 255))
            textSize = self.textGui.size(text[0])
            textSurface = pygame.transform.scale(textSurface, (int(textSize[0]/3), int(textSize[1]/3)))
            textPos = [text[1][0], text[1][1]]
            self.screen.blit(textSurface, self.camera.applyPos(textPos))
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
