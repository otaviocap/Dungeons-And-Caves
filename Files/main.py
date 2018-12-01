'''
WINDOWS
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
15)  zSaveButton.png

UNIX
01) sliderBall.png
02) logo.png
03) characterSelected.png
04) optionsSelected.png
05) arrowLeft.png
06) options.png
07) menuSelected.png
08) menuBackground.png
09) slider.png
10) character.png
11) StartButton.png
12) menu.png
13) arrowRight.png
14) loadButton.png
15) difficulty.png
'''

import pygame
from textEngine import textGui
from glob import glob
from Interpreter import Interpreter
from os import name
from saveGetter import saveGetter
from MenuUI import *
from Game import game
from Sounds import Sound


class Menu():

    def __init__(self):
        self.data = Interpreter()
        self.difficulties = [
            'easy',
            'normal',
            'hard'
        ]
        self.difficultySelected = self.data.getParameter('difficulty')
        self.musicValue = self.data.getParameter('music')
        self.sfxValue =  self.data.getParameter('sfx')
        self.buttons = []
        self.menuButtons = []
        self.bigButtons = []
        self.sliders = []
        self.texts = {}
        self.images = []
        self.logo = pygame.image.load('../Assets/menuAssets/logo.png')
        self.logoPos = [5,0]
        self.animBool = True
        # self.sfxValue = self.data.getParameter('sfx')
        # self.musicValue = self.data.getParameter('music')
        self.loadImages()
        self.mainMenu()
        self.game = game(self)
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
        self.sound = Sound()

    def loadImages(self):
        n = 0
        if name == 'nt':
            for file in glob('../Assets/menuAssets/*.png'):
                self.images.append(pygame.image.load(file))
                print(str(n) + ') ' + file)
                n += 1
            self.images[14], self.images[15] = self.images[15], self.images[14]
        else:
            tempList = []
            for file in glob('../Assets/menuAssets/*.png'):
                tempList.append(file)
            tempList.sort()
            tempList.append(tempList[0])
            tempList.pop(0)
            for file in tempList:
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
            self.texts['Text'] = ['         Unavaible', (385, 230)]
            Button(self, 410, 340, 'self.menu.game.gameRun()', [self.images[15], self.images[15]])
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
            Button(self, 405, 355, image=[self.images[5], self.images[5]], action='self.menu.load()')
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
            a = pygame.image.load('../Assets/me.png')
            a = pygame.transform.scale(a, (int(a.get_rect().width/3), int(a.get_rect().height/3)))
            Button(self, 410, 200, image=[a, a])
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
            self.data.updateParameter('difficulty', self.difficulties[n])
            return self.difficulties[n]

    def load(self):
        for button in self.buttons:
            if button.clicked:
                saveGetter(self.game, button.text, loadind=True)
                self.game.gameRun(button.text)




if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    b = Menu()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for i in range(2):
                    if i == 0:
                        b.data.updateParameter('music', b.musicValue)
                    if i == 1:
                        b.data.updateParameter('sfx', b.sfxValue)
                b.data.updateParameter('difficulty', b.difficulty('return'))
                pygame.quit()
                quit()
        b.update()
        b.draw()
        pygame.display.flip()

