import pygame

class Spike(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h, type):
        self.game = game
        super().__init__()
        self.spikeImg = pygame.image.load('../Assets/Spikes.png')
        self.getStates()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        self.setActive()
        self.rect = pygame.Rect(x, y, w, h)
        self.game.spikes.add(self)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.timer = 120

    def setActive(self):
        if self.type == 'on':
            self.state = 3
            self.active = True
        else:
            self.state = 0
            self.active = False

    def invert(self):
        self.game.menu.sound.playSfx(3)
        self.active = not self.active


    def getRenderImg(self):
        if self.active:
            return 2
        if self.timer <= 60:
            return 1
        else:
            return 0

    def getStates(self):
        self.spikeStates = []
        pos = [0,0]
        for i in range(3):
            self.spikeStates.append(self.spikeImg.subsurface(pos, (16, 16)))
            pos[0] += 17

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False) and self.active and not self.game.player.flying:
            self.time = self.clock.tick()
            if self.time > 20:
                self.game.player.life -= 1
                self.clock.tick()
        for i in self.game.enemies.sprites():
            if pygame.sprite.collide_rect(self, i):
                self.timeEnemy = self.clock.tick()
                if self.timeEnemy > 20:
                    i.life -= 1
                    self.clock.tick()
        if self.timer <= 0:
            self.timer = 120
            self.invert()
        self.timer -= 1

