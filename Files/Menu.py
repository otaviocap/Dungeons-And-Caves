'''
00)  arrowLeft.png
01)  arrowRight.png
02)  character.png
03)  characterSelected.png
04)  difficulty.png
05)  loadButton.png
06)  logo.png
07)  menu.png
08)  menuBackground.png
09)  menuSelected.png
10)  options.png
11)  optionsSelected.png
12)  slider.png
13)  sliderBall.png
14)  StartButton.png
'''

import pygame
from textEngine import textGui
from glob import glob

class Menu():

    def __init__(self):
        self.images = []
        self.buttons = []
        self.menuButtons = []
        self.bigButtons = []
        self.sliders = []
        self.logo = pygame.image.load('../Assets/menuAssets/logo.png')
        self.logoPos = [5,0]
        self.animBool = True
        self.loadImages()
        self.mainMenu()
        self.textGui = textGui()
        self.menuPage = {
            'new': False,
            'load': False,
            'options': False,
            'credits': False,
            'quit': False
        }
        self.screen = pygame.display.set_mode((720, 480))
        self.backgroundMenu = False

    def loadImages(self):
        for file in glob('..\Assets\menuAssets\*.png'):
            self.images.append(pygame.image.load(file))
            print(file)

    def mainMenu(self):
        Button(self, 0, 0, 'New Game', 'new', 'menuButtons')
        Button(self, 0, 0, 'Load Game', 'load', 'menuButtons')
        Button(self, 0, 0, 'Options', 'options', 'menuButtons')
        Button(self, 0, 0, 'Credits', 'credits', 'menuButtons')
        Button(self, 0, 0, 'Quit', 'quit', 'menuButtons')

        # Slider(self, 100, 400, 0, 10)
        # Slider(self, 100, 430, 0, 10)

    def draw(self):
        self.screen.fill((28, 17, 23))
        if self.backgroundMenu:
            self.screen.blit(self.images[8], (350, 50))
        pos = [10, 180]
        for i in self.menuButtons:
            i.x = pos[0]
            i.y = pos[1]
            i.draw()
            pos[1] += 60
        for i in self.sliders:
            i.draw()
        for i in self.bigButtons:
            i.draw()
        self.screen.blit(self.logo, self.logoPos)

    def update(self):
        for button in self.menuButtons:
            button.update()
        for slider in self.sliders:
            slider.update()
        for button in self.bigButtons:
            button.update()
        if self.animBool:
            self.logoPos[1] += 0.5
        else:
            self.logoPos[1] -= 0.5
        if self.logoPos[1] == 20 or self.logoPos[1] == 0:
            self.animBool = not self.animBool
        if self.menuPage['new']:
            self.newPage()
        elif self.menuPage['load']:
            self.loadPage()
        elif self.menuPage['options']:
            self.optionsPage()
        elif self.menuPage['credits']:
            self.creditsPage()
        elif self.menuPage['quit']:
            self.quitPage()
        else:
            self.backgroundMenu = False

    def newPage(self):
        self.backgroundMenu = True
        bigButton(self, 300, 200, ['../Assets/character1.png'])
        bigButton(self, 450, 200, ['../Assets/character1.png', '../Assets/character2.png'])

    def loadPage(self):
        self.clear()
        self.backgroundMenu = True

    def optionsPage(self):
        self.clear()
        self.backgroundMenu = True

    def creditsPage(self):
        self.clear()
        self.backgroundMenu = True

    def quitPage(self):
        self.clear()
        self.backgroundMenu = True

    def clear(self):
        self.bigButtons.clear()
        self.sliders.clear()
        self.buttons.clear()

    def run(self):
        self.update()
        self.draw()


class Button:

    def __init__(self, menu, x, y, text, key, group):
        self.menu = menu
        self.key = key
        self.group = group
        exec('self.menu.'+group+'.append(self)')
        self.text = text
        self.images = [self.menu.images[7], self.menu.images[9]]
        self.renderImage = self.images[0]
        self.x = x
        self.y = y
        self.w = self.images[0].get_rect().size[0]
        self.h = self.images[0].get_rect().size[1]
        self.rect = self.images[0].get_rect()
        self.clicked = False
        self.selected = False
        self.cooldown = 0

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y:
            self.setSelected(True)
            if self.cooldown <= 0:
                if self.isClicked():
                    self.disarmOthers()
                    self.clicked = not self.clicked
                    self.menu.menuPage[self.key] = not self.menu.menuPage[self.key]
                    self.cooldown = 10
                    print('Teste')
        else:
            self.setSelected(False)

        if self.selected or self.clicked:
            self.renderImage = self.images[1]
        else:
            self.renderImage = self.images[0]
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def setSelected(self, bool):
        if bool:
            self.selected = bool
        else:
            self.selected = bool

    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def disarmOthers(self):
        for key in self.menu.menuPage.keys():
            if key != self.key:
                self.menu.menuPage[key] = False
        if self.group == 'menuButtons':
            for button in self.menu.menuButtons:
                if button != self:
                 button.clicked = False
        else:
            for button in self.menu.buttons:
                if button != self:
                 button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text)*7.5, self.rect.center[1] - 20))


class Slider:

    def __init__(self, menu, x, y, max, min):
        self.menu = menu
        self.max = max
        self.min = min
        self.x = x
        self.y = y
        self.images = [self.menu.images[12], self.menu.images[13]]
        self.rectBall = self.images[1].get_rect()
        self.rectSlide = self.images[0].get_rect()
        self.rectBall.x = self.x
        self.rectBall.y = self.y
        self.rectSlide.x = self.x
        self.rectSlide.y = self.y
        self.spawnX = x
        self.spawnY = y
        self.dragging = False
        self.menu.sliders.append(self)
        self.mouse = pygame.Rect(pygame.mouse.get_pos(), (30, 50))

    def update(self):
        self.mouse.x = pygame.mouse.get_pos()[0]
        self.mouse.y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[0] and pygame.Rect.colliderect(self.rectBall, self.mouse):
            self.dragging = True
        else:
            self.dragging = False
        if self.dragging:
            if self.mouse[0] - self.spawnX >= -2 and self.mouse[0] - self.spawnX <= 255:
                self.rectBall.x = self.mouse[0]

    def getValue(self):
        return self.mapping(self.rectBall.x-self.spawnX, -2, 255, 0, 100)

    def draw(self):
        self.menu.screen.blit(self.images[0], (self.x, self.y))
        self.menu.screen.blit(self.images[1], (self.rectBall.x, self.rectBall.y - 5))
        # pygame.draw.rect(self.menu.screen, (255,255,255), (self.rectSlide.x, self.rectSlide.y, self.rectSlide.width, self.rectSlide.height))

    def mapping(self, x, inMin, inMax, outMin=None, outMax=None):
        if outMin == None and outMax == None:
            outMin, outMax = self.max, self.min
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;


class bigButton:

    def __init__(self, menu, x, y, images):
        self.menu = menu
        self.images = [self.menu.images[2], self.menu.images[3]]
        self.menu.bigButtons.append(self)
        self.renderImage = self.images[0]
        self.addImage = []
        for i in images:
            a = pygame.image.load(i)
            a = pygame.transform.scale(a, (a.get_rect().width * 3, a.get_rect().height * 3))
            self.addImage.append(a)
        self.x = x
        self.y = y
        self.w = self.images[0].get_rect().size[0]
        self.h = self.images[0].get_rect().size[1]
        self.rect = self.images[0].get_rect()
        self.clicked = False
        self.selected = False
        self.cooldown = 0

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y:
            self.setSelected(True)
            if self.cooldown <= 0:
                if self.isClicked():
                    self.disarmOthers()
                    self.clicked = not self.clicked
                    self.cooldown = 10
                    print('Teste')
        else:
            self.setSelected(False)

        if self.selected or self.clicked:
            self.renderImage = self.images[1]
        else:
            self.renderImage = self.images[0]
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def setSelected(self, bool):
        if bool:
            self.selected = bool
        else:
            self.selected = bool

    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def disarmOthers(self):
        for button in self.menu.bigButtons:
            if button != self:
                button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        if len(self.addImage) == 2:
            self.menu.screen.blit(self.addImage[0], (self.rect.center[0] - 50, self.rect.center[1] - 20))
            self.menu.screen.blit(self.addImage[1], (self.rect.center[0] + 10, self.rect.center[1] - 20))
        elif len(self.addImage) == 1:
            self.menu.screen.blit(self.addImage[0], (self.rect.center[0] - 20, self.rect.center[1] - 20))

if __name__ == '__main__':
    pygame.init()
    a = Menu()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        a.update()
        a.draw()
        pygame.display.flip()

