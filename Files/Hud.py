import pygame
from textEngine import *


class Hud:

    def __init__(self, game):
        self.game = game
        self.heartImg = pygame.image.load('../Assets/heart.png')
        self.heartBossImg = pygame.image.load('../Assets/heartBoss.png')
        self.textEngine = textGui()
        dieText = self.textEngine.text('You Died', color=(140, 0, 0), antialias=False, background=(255,255,255))
        dieText.set_colorkey((255,255,255))
        self.dieText = pygame.transform.scale(dieText, (295, 120))
        self.dieText.convert_alpha()
        self.cooldownRect = pygame.Rect((10, 475), (3, 3))
        self.effectRect = pygame.Rect((10, 435), (3, 3))
        self.deathAlpha = 0
        self.getStates()
        self.counter = 0
        self.youDied = False

    def getStates(self):
        self.heartStages = []
        self.heartStages.append(self.heartImg.subsurface((0, 0, 13, 12)))
        self.heartStages.append(self.heartImg.subsurface((16, 0, 13, 12)))
        self.heartStages.append(self.heartImg.subsurface((32, 0, 13, 12)))
        for i in range(3):
            self.heartStages[i] = pygame.transform.scale(self.heartStages[i], (26, 24))
        self.heartBossStages = []
        self.heartBossStages.append(self.heartBossImg.subsurface((0, 0, 13, 12)))
        self.heartBossStages.append(self.heartBossImg.subsurface((16, 0, 13, 12)))
        self.heartBossStages.append(self.heartBossImg.subsurface((32, 0, 13, 12)))
        for i in range(3):
            self.heartBossStages[i] = pygame.transform.scale(self.heartBossStages[i], (26, 24))

    def update(self):
        self.life = self.game.player.life
        self.fullHearts, self.halfHearts, self.emptyHearts = 0, 0, 0
        for i in range(int(self.game.player.maxLife / 2)):
            if self.life >= 2:
                self.fullHearts += 1
                self.life -= 2
            elif self.life >= 1:
                self.halfHearts += 1
                self.life -= 1
            else:
                self.emptyHearts += 1
        self.cooldownRect.width = self.getValue(self.game.player.bookMagicCooldown, self.game.player.bookMagicCooldownDefault)
        self.effectRect.width = self.getValue(self.game.player.effectTime, self.game.player.effectTimeDefault)


    def draw(self):
        space = 0
        for _ in range(self.fullHearts):
            self.game.screen.blit(self.heartStages[0], (space, 0))
            space += 30
        for _ in range(self.halfHearts):
            self.game.screen.blit(self.heartStages[1], (space, 0))
            space += 30
        for _ in range(self.emptyHearts):
            self.game.screen.blit(self.heartStages[2], (space, 0))
            space += 30
        if self.game.player.effectTime != 0:
            bookImg = self.game.player.bookImg[1]
        else:
            bookImg = self.game.player.bookImg[0]
        bookImg = pygame.transform.scale(bookImg, (32, 32))
        self.game.screen.blit(bookImg, (10, 440))

        if self.effectRect.width == 1:
            pass
        else:
            pygame.draw.rect(self.game.screen, (255, 0, 0), self.effectRect)

        if self.cooldownRect.width == 1:
            pass
        else:
            pygame.draw.rect(self.game.screen, (0, 255, 0), self.cooldownRect)
        if self.game.player.life == 0:
            pass
            '''
            self.deathScreen()
            if not self.youDied:
                self.game.menu.sound.playSfx(2)
                self.youDied = True
            if self.counter == 70:
                self.game.done = True
                self.game.gameRun(self.game.saveName)
            '''

    def getValue(self, x, inMax):
        x = x
        inMin = 0
        inMax = inMax
        outMin = 1
        outMax = 30
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

    def deathScreen(self):
        if self.deathAlpha < 200:
            self.deathAlpha += 2
        else:
            self.counter += 1
        deathSurface = pygame.Surface((self.game.screenSize[0], self.game.screenSize[1] -340))
        deathSurface.fill((0,0,0))
        deathSurface.set_alpha(self.deathAlpha)
        self.dieText.set_alpha(self.deathAlpha)
        self.game.screen.blit(deathSurface, (0, 175))
        self.game.screen.blit(self.dieText, (225, 175))

