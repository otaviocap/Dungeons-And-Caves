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
from Interpreter import Interpreter
from main import game

class Menu():

    def __init__(self):

        self.data = Interpreter()
        self.difficulties = [
            'easy',
            'normal',
            'hard',
        ]
        self.difficultySelected = self.data.getParameter('difficulty')
        self.buttons = []
        self.menuButtons = []
        self.bigButtons = []
        self.sliders = []
        self.texts = {}
        self.images = []
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
        menuButton(self, 0, 0, 'New Game', 'new', 'menuButtons')
        menuButton(self, 0, 0, 'Load Game', 'load', 'menuButtons')
        menuButton(self, 0, 0, 'Options', 'options', 'menuButtons')
        menuButton(self, 0, 0, 'Credits', 'credits', 'menuButtons')
        menuButton(self, 0, 0, 'Quit', 'quit', 'menuButtons')

    def draw(self):
        self.screen.fill((28, 17, 23))
        if self.backgroundMenu:
            self.screen.blit(self.images[8], (350, 50))
        pos = [10, 180]
        for buttons in self.menuButtons:
            buttons.x = pos[0]
            buttons.y = pos[1]
            buttons.draw()
            pos[1] += 60
        for buttons in self.buttons:
            buttons.draw()
        for sliders in self.sliders:
            sliders.draw()
        for buttons in self.bigButtons:
            buttons.draw()
        for key, text in self.texts.items():
            if key == 'difficulty':
                self.screen.blit(self.textGui.text(self.difficulty('return'), color=(28, 17, 23)), text[1])
            else:
                self.screen.blit(self.textGui.text(text[0], color=(28, 17, 23)), text[1])
        self.screen.blit(self.logo, self.logoPos)

    def update(self):
        for button in self.menuButtons:
            button.update()
        for button in self.bigButtons:
            button.update()
        for button in self.buttons:
            button.update()
        for slider in self.sliders:
            slider.update()
        if self.animBool:
            self.logoPos[1] += 0.5
        else:
            self.logoPos[1] -= 0.5
        if self.logoPos[1] == 20 or self.logoPos[1] == 0:
            self.animBool = not self.animBool
        x = True
        for i in self.menuPage.keys():
            if self.menuPage[i]:
                x = False
        if x:
            self.clear()
            self.backgroundMenu = False

    def newPage(self):
        if not self.menuPage['new']:
            self.clear()
            self.backgroundMenu = True
            bigButton(self, 370, 70, ['../Assets/character1.png'], '1 Player')
            bigButton(self, 520, 70, ['../Assets/character1.png', '../Assets/character2.png'], '2 Players')
            self.textGui.text('1 Player    2 Players')
            Button(self, 410, 340, 'game().gameRun()', [self.images[14], self.images[14]])
            self.menuPage['new'] = True
        else:
            self.menuPage['new'] = False

    def loadPage(self):
        if not self.menuPage['load']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[10], self.images[11]], text='Slot 1', selectable=True)
            Button(self, 365, 155, image=[self.images[10], self.images[11]], text='Slot 2', selectable=True)
            Button(self, 365, 240, image=[self.images[10], self.images[11]], text='Slot 3', selectable=True)
            Button(self, 405, 355, image=[self.images[5], self.images[5]])
            self.menuPage['load'] = True
        else:
            self.menuPage['load'] = False

    def optionsPage(self):
        if not self.menuPage['options']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Music')
            Slider(self, 370, 155, 0, 100, 'musicP')
            Button(self, 365, 200, image=[self.images[11], self.images[11]], text='Sound Effects')
            Slider(self, 370, 285, 0, 100, 'sfxP')
            Button(self, 365, 320, image=[self.images[11], self.images[11]], text='Difficulty')
            Button(self, 375, 400, image=[self.images[4], self.images[4]])
            Button(self, 385, 401, image=[self.images[0], self.images[0]], action='self.menu.difficulty("down")')
            Button(self, 625, 401, image=[self.images[1], self.images[1]], action='self.menu.difficulty("up")')
            self.texts['difficulty'] = ('', (461, 391))
            self.menuPage['options'] = True
        else:
            self.menuPage['options'] = False

    def creditsPage(self):
        if not self.menuPage['credits']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Made By:')
            self.texts['credit1'] = ('Otávio H. G. C.', (410, 150))
            self.texts['credit2'] = ('(otaviocap)', (435, 180))
            self.menuPage['credits'] = True
        else:
            self.menuPage['credits'] = False

    def quitPage(self):
        if not self.menuPage['quit']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Quit?')
            Button(self, 365, 70*4, image=[self.images[10], self.images[11]], text='Yes ;-;', action='pygame.event.post(pygame.event.Event(pygame.QUIT))')
            Button(self, 365, 73*5, image=[self.images[10], self.images[11]], text='No :)')
            self.menuPage['quit'] = True
        else:
            self.menuPage['quit'] = False

    def clear(self):
        self.bigButtons.clear()
        self.sliders.clear()
        self.buttons.clear()
        self.texts.clear()

    def run(self):
        self.update()
        self.draw()

    def difficulty(self, up):
        min = -len(self.difficulties)
        max = len(self.difficulties)
        n = 0
        for i in range(len(self.difficulties)):
            if self.difficultySelected == self.difficulties[i]:
                n = i
        if up == 'up':
            n += 1
            if n >= max:
                n = 0
        elif up == 'down':
            n -= 1
            if n <= min:
                n = len(self.difficulties)
        try:
            self.difficultySelected = self.difficulties[n]
        except:
            self.difficultySelected = self.difficulties[0]
        if up == 'return':
            return self.difficulties[n]



class menuButton:

    def __init__(self, menu, x, y, text='', key='', group=''):
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
        self.helper = False

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
                    exec('self.menu.'+self.key+'Page()')
                    self.cooldown = 10
                    print('self.menu.'+self.key+'Page()')
                    self.helper = True
        else:
            self.setSelected(False)
            if self.key == 'options' and self.helper:
                print('sad')
                for i in range(len(self.menu.sliders)):
                    a = self.menu.sliders[i].getValue()
                    if i == 0:
                        self.menu.data.updateParameter('music', a)
                    if i == 1:
                        self.menu.data.updateParameter('sfx', a)
                self.menu.data.updateParameter('difficulty', self.menu.difficulty('return'))
                self.helper = False

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
        self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text)*7.5, self.rect.center[1] - 25))


class Slider:

    def __init__(self, menu, x, y, max, min, keyForPos=None):
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

    def __init__(self, menu, x, y, images, text=''):
        self.menu = menu
        self.text = text
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
            self.menu.screen.blit(self.addImage[0], (self.x+25, self.y+40))
            self.menu.screen.blit(self.addImage[1], (self.x+75, self.y+40))
        elif len(self.addImage) == 1:
            self.menu.screen.blit(self.addImage[0], (self.x+45, self.y+40))
        self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text) * 7.5, self.rect.center[1] + 60))


class Button:

    def __init__(self, menu, x, y, action='', image=None, text=None, selectable=False):
        self.menu = menu
        self.action = action
        self.menu.buttons.append(self)
        self.text = text
        self.selectable = selectable
        if image == None:
            self.images = [self.menu.images[7], self.menu.images[9]]
        else:
            self.images = image
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
                    if self.selectable:
                        self.disarmOthers()
                        self.clicked = not self.clicked
                    exec(self.action)
                    self.cooldown = 10
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
        for button in self.menu.buttons:
            if button != self:
                button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        if self.text != None:
            self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text) * 7.5, self.rect.center[1] - 25))



if __name__ == '__main__':
    pygame.init()
    a = Menu()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        a.update()
        a.draw()
        pygame.display.flip()

